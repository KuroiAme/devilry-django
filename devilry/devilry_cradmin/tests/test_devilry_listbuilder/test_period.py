# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import htmls
from django import test
from django.conf import settings
from django_cradmin import datetimeutils
from model_mommy import mommy

from devilry.apps.core.models import Period
from devilry.devilry_cradmin import devilry_listbuilder


class TestAdminItemValue(test.TestCase):
    def test_custom_cssclass(self):
        testperiod = mommy.make('core.Period')
        selector = htmls.S(devilry_listbuilder.period.AdminItemValue(value=testperiod).render())
        self.assertTrue(selector.exists('.devilry-cradmin-perioditemvalue-admin'))

    def test_title(self):
        testperiod = mommy.make('core.Period', long_name='Test Period')
        selector = htmls.S(devilry_listbuilder.period.AdminItemValue(value=testperiod).render())
        self.assertEqual(
                'Test Period',
                selector.one('.django-cradmin-listbuilder-itemvalue-titledescription-title').alltext_normalized)

    def test_description(self):
        testperiod = mommy.make('core.Period',
                                start_time=datetimeutils.default_timezone_datetime(2015, 1, 15),
                                end_time=datetimeutils.default_timezone_datetime(2015, 12, 24))
        selector = htmls.S(devilry_listbuilder.period.AdminItemValue(value=testperiod).render())
        self.assertEqual(
                'Thursday January 15, 2015, 00:00 \u2014 Thursday December 24, 2015, 00:00',
                selector.one('.django-cradmin-listbuilder-itemvalue-titledescription-description').alltext_normalized)


class TestStudentItemValue(test.TestCase):
    def test_custom_cssclass(self):
        testperiod = mommy.make('core.Period')
        selector = htmls.S(devilry_listbuilder.period.StudentItemValue(value=testperiod).render())
        self.assertTrue(selector.exists('.devilry-cradmin-perioditemvalue-student'))

    def test_title(self):
        testperiod = mommy.make('core.Period',
                                parentnode__long_name='Test Subject',
                                long_name='Test Period')
        selector = htmls.S(devilry_listbuilder.period.StudentItemValue(value=testperiod).render())
        self.assertEqual(
                'Test Subject - Test Period',
                selector.one('.django-cradmin-listbuilder-itemvalue-titledescription-title').alltext_normalized)

    def test_description_no_assignments(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testperiod = mommy.make('core.Period')
        testperiod_annotated = Period.objects\
            .extra_annotate_with_assignmentcount_for_studentuser(user=testuser)\
            .get(id=testperiod.id)
        selector = htmls.S(devilry_listbuilder.period.StudentItemValue(value=testperiod_annotated).render())
        self.assertEqual(
                '0 assignments',
                selector.one('.django-cradmin-listbuilder-itemvalue-titledescription-description').alltext_normalized)

    def test_description_single_assignment(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testperiod = mommy.make('core.Period')
        relatedstudent = mommy.make('core.RelatedStudent', user=testuser, period=testperiod)
        testassignment = mommy.make('core.Assignment', parentnode=testperiod)
        mommy.make('core.Candidate',
                   assignment_group__parentnode=testassignment,
                   relatedstudent=relatedstudent)
        testperiod_annotated = Period.objects\
            .extra_annotate_with_assignmentcount_for_studentuser(user=testuser)\
            .get(id=testperiod.id)
        selector = htmls.S(devilry_listbuilder.period.StudentItemValue(value=testperiod_annotated).render())
        self.assertEqual(
                '1 assignment',
                selector.one('.django-cradmin-listbuilder-itemvalue-titledescription-description').alltext_normalized)

    def test_description_multiple_assignments_assignment(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL)
        testperiod = mommy.make('core.Period')
        relatedstudent = mommy.make('core.RelatedStudent', user=testuser, period=testperiod)
        testassignment1 = mommy.make('core.Assignment', parentnode=testperiod)
        mommy.make('core.Candidate',
                   assignment_group__parentnode=testassignment1,
                   relatedstudent=relatedstudent)
        testassignment2 = mommy.make('core.Assignment', parentnode=testperiod)
        mommy.make('core.Candidate',
                   assignment_group__parentnode=testassignment2,
                   relatedstudent=relatedstudent)
        testperiod_annotated = Period.objects\
            .extra_annotate_with_assignmentcount_for_studentuser(user=testuser)\
            .get(id=testperiod.id)
        selector = htmls.S(devilry_listbuilder.period.StudentItemValue(value=testperiod_annotated).render())
        self.assertEqual(
                '2 assignments',
                selector.one('.django-cradmin-listbuilder-itemvalue-titledescription-description').alltext_normalized)
