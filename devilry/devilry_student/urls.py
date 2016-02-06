from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django_cradmin import crinstance

from devilry.devilry_student.views.group.projectgroupapp import GroupInviteRespondView
from devilry.devilry_student.views.dashboard import crinstance_dashboard
from devilry.devilry_student.views.period import crinstance_period

@login_required
def redirect_to_student_frontpage_view(request):
    return redirect(crinstance.reverse_cradmin_url(
        instanceid='devilry_student',
        appname='waitingfordeliveries',
        roleid=request.user.id))


urlpatterns = patterns(
    'devilry.devilry_student',
    url('^$', redirect_to_student_frontpage_view, name='devilry_student'),

    url(r'^groupinvite/respond/(?P<invite_id>\d+)$',
        login_required(GroupInviteRespondView.as_view()),
        name='devilry_student_groupinvite_respond'),

    url(r'^show_delivery/(?P<delivery_id>\d+)$', 'views.show_delivery.show_delivery',
        name='devilry_student_show_delivery'),

    url(r'^period/', include(crinstance_period.CrAdminInstance.urls())),
    url(r'^', include(crinstance_dashboard.CrAdminInstance.urls()))
)
