from __future__ import unicode_literals

from crispy_forms import layout
from django import forms
from django.http import Http404
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy
from django_cradmin import crapp
from django_cradmin.crispylayouts import PrimarySubmit
from django_cradmin.viewhelpers import formbase
from django_cradmin.viewhelpers import listbuilder
from django_cradmin.viewhelpers import listbuilderview

from devilry.apps.core.models import Assignment
from devilry.apps.core.models import Period
from devilry.utils.passed_in_previous_period import PassedInPreviousPeriod


class SelectPeriodForm(forms.Form):
    semester = forms.ModelChoiceField(
        widget=forms.RadioSelect(),
        queryset=Period.objects.none()
    )

    def __init__(self, *args, **kwargs):
        period_queryset = kwargs.pop('period_queryset')
        super(SelectPeriodForm, self).__init__(*args, **kwargs)
        self.fields['semester'].queryset = period_queryset
        self.fields['semester'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        return "{} - {}".format(obj.short_name, obj.long_name)


class SelectPeriodView(formbase.FormView):
    form_class = SelectPeriodForm
    template_name = 'devilry_admin/assignment/students/passed_previous_period/select-period-view.django.html'

    def dispatch(self, request, *args, **kwargs):
        self.assignment = self.request.cradmin_role
        self.devilryrole = self.request.cradmin_instance.get_devilryrole_for_requestuser()
        if self.assignment.is_fully_anonymous and self.devilryrole != 'departmentadmin':
            raise Http404()
        if self.assignment.is_semi_anonymous and self.devilryrole == 'periodadmin':
            raise Http404()
        return super(SelectPeriodView, self).dispatch(request, *args, **kwargs)

    def get_pagetitle(self):
        return ugettext_lazy('Select the earliest semester you want to approve for')

    def __get_period_queryset(self):
        return Period.objects.filter(
            parentnode=self.assignment.parentnode.parentnode,
            assignments__short_name=self.assignment.short_name
        ).prefetch_related('assignments')\
            .exclude(start_time__gte=self.assignment.parentnode.start_time)\
            .order_by('start_time')

    def get_button_layout(self):
        return [
            PrimarySubmit('Next', ugettext_lazy('Next'))
        ]

    def get_field_layout(self):
        return [
            layout.Div('semester', css_class='')
        ]

    def form_valid(self, form):
        period = form.cleaned_data['semester']
        return redirect(self.get_redirect_url(period))

    def get_form_kwargs(self):
        kwargs = super(SelectPeriodView, self).get_form_kwargs()
        kwargs['period_queryset'] = self.__get_period_queryset()
        return kwargs
    
    def get_context_data(self, **kwargs):
        return super(SelectPeriodView, self).get_context_data(**kwargs)

    def get_redirect_url(self, period):
        return self.request.cradmin_app.reverse_appurl(
            'assignments',
            kwargs={'period_id': period.id}
        )


class AssignmentItemValue(listbuilder.itemvalue.TitleDescription):
    template_name = 'devilry_admin/assignment/students/passed_previous_period/assignment-item-value.django.html'

    def __init__(self, **kwargs):
        super(AssignmentItemValue, self).__init__(**kwargs)
        self.period_start = self.value.parentnode.start_time
        self.period_end = self.value.parentnode.end_time
        self.max_points = self.value.max_points
        self.passing_grade_min_points = self.value.passing_grade_min_points

    def get_title(self):
        return '{} - {}'.format(self.value.long_name, self.value.parentnode.long_name)


class PassedPreviousAssignmentView(listbuilderview.View):
    model = Assignment
    template_name = 'devilry_admin/assignment/students/passed_previous_period/assignment-overview.django.html'
    value_renderer_class = AssignmentItemValue

    def dispatch(self, request, *args, **kwargs):
        self.period = Period.objects.get(id=kwargs.pop('period_id'))
        self.assignment = self.request.cradmin_role
        self.devilryrole = self.request.cradmin_instance.get_devilryrole_for_requestuser()
        if self.assignment.is_fully_anonymous and self.devilryrole != 'departmentadmin':
            raise Http404()
        if self.assignment.is_semi_anonymous and self.devilryrole == 'periodadmin':
            raise Http404()
        return super(PassedPreviousAssignmentView, self).dispatch(request, *args, **kwargs)

    def get_queryset_for_role(self, role):
        return self.model.objects.filter(
            short_name=role.short_name,
            parentnode__start_time__gte=self.period.start_time,
            parentnode__end_time__lt=self.assignment.period.end_time,
            parentnode__parentnode=self.assignment.parentnode.parentnode
        ).select_related('parentnode__parentnode')

    def get_pagetitle(self):
        return ugettext_lazy('Confirm assignmnets')

    def get_context_data(self, **kwargs):
        context = super(PassedPreviousAssignmentView, self).get_context_data(**kwargs)
        context['period_id'] = self.period.id
        return context


class CandidateItemValue(listbuilder.itemvalue.TitleDescription):
    template_name = 'devilry_admin/assignment/students/passed_previous_period/candidate-item-value.django.html'

    def __init__(self, **kwargs):
        self.current_assignment = kwargs.pop('current_assignment')
        self.devilryrole = kwargs.pop('devilryrole')
        self.util_class = kwargs.pop('util_class')
        super(CandidateItemValue, self).__init__(**kwargs)
        self.assignment = self.value.assignment_group.parentnode
        self.period = self.value.assignment_group.parentnode.parentnode
        self.feedback = self.value.assignment_group.cached_data.last_published_feedbackset
        self.calculated_points = self.util_class.convert_points(self.feedback)


class CandidateListbuilder(listbuilder.base.List):

    def __init__(self, current_assignment, devilryrole, util_class):
        super(CandidateListbuilder, self).__init__()
        self.current_assignment = current_assignment
        self.devilry_role = devilryrole
        self.util_class = util_class

    def __get_candidate_queryset(self):
        return self.util_class.get_queryset()

    def build(self):
        self.extend_with_values(
            value_iterable=self.__get_candidate_queryset(),
            value_renderer_class=CandidateItemValue,
            value_and_frame_renderer_kwargs={
                'current_assignment': self.current_assignment,
                'devilryrole': self.devilry_role,
                'util_class': self.util_class
            })


class ApprovePreviousAssignments(formbase.FormView):
    form_class = forms.Form
    template_name = 'devilry_admin/assignment/students/passed_previous_period/confirm-view.django.html'

    def dispatch(self, request, *args, **kwargs):
        self.period = Period.objects.get(id=kwargs.pop('period_id'))
        self.assignment = self.request.cradmin_role
        self.devilryrole = self.request.cradmin_instance.get_devilryrole_for_requestuser()
        self.util_class = PassedInPreviousPeriod(self.assignment, self.period)
        if self.assignment.is_fully_anonymous and self.devilryrole != 'departmentadmin':
            raise Http404()
        if self.assignment.is_semi_anonymous and self.devilryrole == 'periodadmin':
            raise Http404()
        return super(ApprovePreviousAssignments, self).dispatch(request, *args, **kwargs)

    def get_pagetitle(self):
        return ugettext_lazy('Approve assignments')

    def __get_candidate_listbuilder(self):
        listbuilder = CandidateListbuilder(self.assignment, self.devilryrole, self.util_class)
        listbuilder.build()
        return listbuilder

    def get_context_data(self, **kwargs):
        context = super(ApprovePreviousAssignments, self).get_context_data(**kwargs)
        context['period_id'] = self.period.id
        context['candidate_list'] = self.__get_candidate_listbuilder()
        return context

    def get_button_layout(self):
        return [
            PrimarySubmit('Confirm', ugettext_lazy('Confirm'))
        ]

    def get_field_layout(self):
        return [
        ]

    def form_valid(self, form):
        #: TODO: implement this
        return super(ApprovePreviousAssignments, self).form_valid(form)


class App(crapp.App):
    appurls = [
        crapp.Url(r'^$', SelectPeriodView.as_view(), name=crapp.INDEXVIEW_NAME),
        crapp.Url(r'^assignment/(?P<period_id>\d+)$', PassedPreviousAssignmentView.as_view(), name='assignments'),
        crapp.Url(r'^confirm/(?P<period_id>\d+)$', ApprovePreviousAssignments.as_view(), name='confirm')
    ]
