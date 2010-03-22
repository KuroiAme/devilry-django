from os.path import basename
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django import forms
from django.forms.formsets import formset_factory
from devilry.core.models import (Delivery, Feedback, AssignmentGroup,
        Node, Subject, Period, Assignment, FileMeta)
from devilry.core import gradeplugin_registry
from django.db import transaction

from devilry.core.utils.GroupNodes import group_assignments, group_assignmentgroups 

from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

@login_required
def list_assignments(request):
    assignments = Assignment.where_is_examiner(request.user)
    all_courses = group_assignmentgroups(assignments)

    if assignments.count() == 0:
        return HttpResponseForbidden("You are not registered as examiner on any assignments.")
    return render_to_response('devilry/examiner/show_assignments.django.html', {
        'assignments': assignments,
        }, context_instance=RequestContext(request))


@login_required
def list_assignmentgroups(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    assignment_groups = assignment.assignment_groups_where_is_examiner(request.user)
    
    return render_to_response('devilry/examiner/list_assignmentgroups.django.html', {
        'assignment_groups': assignment_groups,
        'assignment': assignment_groups[0].parentnode,
        }, context_instance=RequestContext(request))


@login_required
def show_assignmentgroup(request, assignmentgroup_id):
    assignment_group = get_object_or_404(AssignmentGroup, pk=assignmentgroup_id)
    if not assignment_group.is_examiner(request.user):
        return HttpResponseForbidden("Forbidden")
    return render_to_response('devilry/examiner/show_assignmentgroup.django.html', {
        'assignment_group': assignment_group,
        }, context_instance=RequestContext(request))


@login_required
def list_deliveries(request):
    return render_to_response('devilry/studentview/list_deliveries.django.html', {
        'deliveries': Delivery.where_is_student(request.user),
        }, context_instance=RequestContext(request))


@login_required
def correct_delivery(request, delivery_id):
    delivery_obj = get_object_or_404(Delivery, pk=delivery_id)
    if not delivery_obj.assignment_group.is_examiner(request.user):
        return HttpResponseForbidden("Forbidden")
    key = delivery_obj.assignment_group.parentnode.grade_plugin
    return gradeplugin_registry.get(key).view(request, delivery_obj)




@login_required
def choose_assignment(request):
    assignment_pks = AssignmentGroup.where_is_examiner(request.user).values("parentnode").distinct().query
    assignments = Assignment.objects.filter(pk__in=assignment_pks)
    
    subjects = group_assignments(assignments)
    return render_to_response('devilry/examiner/choose_assignment.django.html', {
            'subjects': subjects,
            }, context_instance=RequestContext(request))
