from datetime import datetime
from django.template.loader import render_to_string
from django.template import RequestContext
from django.db.models import Max

from ..core.models import AssignmentGroup

from utils import filter_not_corrected



class ExaminerImportantItem(object):
    sessionid = None

    def __init__(self, request):
        self.request = request
        self.savesession = False
        self.sessionprefix = "dashboard_examiner_" + self.sessionid + "_"
        self.groups, self.total = self.filter()
        if self.savesession:
            self.request.session.save()

    def _querystring_to_sessionbool(self, s):
        value = self.request.GET.get(s)
        if value:
            v = value == "yes"
            self.request.session[s] = v
            self.savesession = True
            return v
        return self.request.session.get(s, False)

    def _handle_buttons(self, groups):
        orderdesc = self._querystring_to_sessionbool(
                self.sessionprefix + "orderdesc")
        orderprefix = ""
        if orderdesc:
            orderprefix = "-"
        groups = groups.order_by(
                orderprefix + 'time_of_last_delivery')
        return groups

    def _handle_limit(self, groups):
        showall = self._querystring_to_sessionbool(
                self.sessionprefix + "showall")
        if not showall:
            groups = groups[:3]
        return groups


    def __len__(self):
        return self.total

    def render(self, request):
        from ...utils.GroupNodes import group_assignmentgroups
        if self.total > 0:
            subjects = group_assignmentgroups(self.groups)
            if isinstance(self.groups, list):
                groupcount = len(self.groups)
            else:
                groupcount = self.groups.count()
            return render_to_string(
                "devilry/examiner/dashboard/%s.django.html" % self.sessionid, {
                    "subjects": subjects,
                    "total": self.total,
                    "groupcount": groupcount
                }, context_instance=RequestContext(request))
        return ""


class NotCorrected(ExaminerImportantItem):
    sessionid = "not_corrected"
    def filter(self):
        not_corrected = filter_not_corrected(self.request.user)
        not_corrected_count = not_corrected.count()
        not_corrected = self._handle_buttons(not_corrected)
        not_corrected = self._handle_limit(not_corrected)
        return not_corrected, not_corrected_count

class NotPublished(ExaminerImportantItem):
    sessionid = "not_published"
    def filter(self):
        groups = AssignmentGroup.active_where_is_examiner(self.request.user)
        not_published = groups.filter(
                is_open=True,
                status=AssignmentGroup.CORRECTED_NOT_PUBLISHED)
        not_published = not_published.annotate(
                active_deadline=Max('deadlines__deadline'),
                time_of_last_delivery=Max('deliveries__time_of_delivery'),
                time_of_last_feedback=Max('deliveries__feedback__last_modified'))
        not_published = not_published.order_by('-time_of_last_feedback')
        not_published_count = not_published.count()
        not_published = self._handle_buttons(not_published)
        not_published = self._handle_limit(not_published)
        return not_published, not_published_count

class CorrectedNotClosed(ExaminerImportantItem):
    sessionid = "not_closed"
    def filter(self):
        groups = AssignmentGroup.active_where_is_examiner(self.request.user)
        not_closed = groups.filter(
                is_open=True,
                status__gt=AssignmentGroup.NO_DELIVERIES)
        not_closed = not_closed.annotate(
                active_deadline=Max('deadlines__deadline'),
                time_of_last_delivery=Max('deliveries__time_of_delivery'),
                time_of_last_feedback=Max('deliveries__feedback__last_modified'))
        not_closed = not_closed.order_by('-time_of_last_feedback')
        not_closed_count = not_closed.count()
        not_closed = self._handle_buttons(not_closed)

        # TODO: Handle this with a query
        groups = []
        for group in not_closed.all():
            if group.time_of_last_feedback:
                if group.time_of_last_delivery > group.time_of_last_feedback:
                    groups.append(group)
        not_closed = self._handle_limit(not_closed)
        return groups, len(groups)

def examiner_important(request, *args, **kwargs):
    not_corrected = NotCorrected(request)
    not_published = NotPublished(request)
    #not_closed = CorrectedNotClosed(request)
    if len(not_corrected) == 0 and len(not_published) == 0:
        return None
    return render_to_string(
        'devilry/examiner/dashboard/examiner_important.django.html', {
            "items": [
                #not_closed.render(request),
                not_corrected.render(request),
                not_published.render(request)]
        }, context_instance=RequestContext(request))
