import mock
from django import test
from django.conf import settings

from model_mommy import mommy
from django_cradmin import cradmin_testhelpers

from devilry.devilry_admin.views.dashboard.student_feedbackfeed_wizard import student_list


class TestStudentListView(test.TestCase, cradmin_testhelpers.TestCaseMixin):
    viewclass = student_list.UserListView

    def test_title(self):
        mockresponse = self.mock_http200_getrequest_htmls()
        self.assertEqual(mockresponse.selector.one('title').alltext_normalized, 'Users')

    def test_list_users(self):
        mommy.make(settings.AUTH_USER_MODEL, shortname='a', fullname='A')
        mommy.make(settings.AUTH_USER_MODEL, shortname='b', fullname='B')
        mommy.make(settings.AUTH_USER_MODEL, shortname='c', fullname='C')
        mockresponse = self.mock_http200_getrequest_htmls()
        fullname_list = [element.alltext_normalized for element in mockresponse.selector.list(
            '.django-cradmin-listbuilder-itemvalue-titledescription-title')]
        shortname_list = [element.alltext_normalized for element in mockresponse.selector.list(
            '.django-cradmin-listbuilder-itemvalue-titledescription-description')]
        self.assertEqual(mockresponse.selector.count('.django-cradmin-listbuilder-itemvalue'), 3)
        self.assertIn('A', fullname_list)
        self.assertIn('B', fullname_list)
        self.assertIn('C', fullname_list)
        self.assertIn('a', shortname_list)
        self.assertIn('b', shortname_list)
        self.assertIn('c', shortname_list)

    def test_search_no_match(self):
        mommy.make(settings.AUTH_USER_MODEL, shortname='a', fullname='A')
        mockresponse = self.mock_http200_getrequest_htmls(
            viewkwargs={'filters_string': 'search-No match'}
        )
        self.assertEqual(0, mockresponse.selector.count('.django-cradmin-listbuilder-itemvalue'))

    def test_search_match_fullname(self):
        mommy.make(settings.AUTH_USER_MODEL, shortname='shortnamea', fullname='FullnameA')
        mockresponse = self.mock_http200_getrequest_htmls(
            viewkwargs={'filters_string': 'search-FullnameA'}
        )
        self.assertEqual(1, mockresponse.selector.count('.django-cradmin-listbuilder-itemvalue'))

    def test_search_match_shortname(self):
        mommy.make(settings.AUTH_USER_MODEL, shortname='shortnamea', fullname='FullnameA')
        mockresponse = self.mock_http200_getrequest_htmls(
            viewkwargs={'filters_string': 'search-shortnamea'}
        )
        self.assertEqual(1, mockresponse.selector.count('.django-cradmin-listbuilder-itemvalue'))

    def test_backlink(self):
        mockresponse = self.mock_http200_getrequest_htmls()
        self.assertEquals(1, len(mockresponse.request.cradmin_instance.reverse_url.call_args_list))
        self.assertEqual(
            mock.call(appname='overview', args=(), kwargs={}, viewname='INDEX'),
            mockresponse.request.cradmin_instance.reverse_url.call_args_list[0]
        )

    def test_user_frame_link(self):
        testuser = mommy.make(settings.AUTH_USER_MODEL, shortname='shortnamea', fullname='FullnameA')
        mockresponse = self.mock_http200_getrequest_htmls()
        self.assertEqual(mockresponse.selector.one('.django-cradmin-listbuilder-itemframe-link')['href'],
                         '/devilry_admin/studentfeedbackfeedwizard/groups/{}'.format(testuser.id))
