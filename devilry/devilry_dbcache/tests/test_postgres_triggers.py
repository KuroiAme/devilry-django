# import unittest
# from datetime import datetime, timedelta
#
# from devilry.apps.core.models import AssignmentGroup
# from devilry.apps.core.mommy_recipes import ACTIVE_PERIOD_START
# from devilry.devilry_comment.models import CommentFile
# from devilry.devilry_dbcache.customsql import AssignmentGroupDbCacheCustomSql
# from devilry.devilry_dbcache.models import AssignmentGroupCachedData
# from devilry.devilry_group import devilry_group_mommy_factories
# from devilry.devilry_group.models import FeedbackSet, GroupComment, ImageAnnotationComment
# from django import test
# from django.conf import settings
# from django.core.files.base import ContentFile
# from django.db import connection
# from django.utils import timezone
# from model_mommy import mommy
#
#
# class TestAssignmentGroupInsertTriggers(test.TestCase):
#     def setUp(self):
#         AssignmentGroupDbCacheCustomSql().initialize()
#
#     def test_create_group_creates_first_feedbackset(self):
#         group = mommy.make('core.AssignmentGroup')
#         self.assertEqual(group.feedbackset_set.count(), 1)
#
#
# class TestAssignmentGroupCachedDataTriggers(test.TestCase):
#     def setUp(self):
#         AssignmentGroupDbCacheCustomSql().initialize()
#
#     def test_autocreated_feedbackset_is_correctly_cached(self):
#         group = mommy.make('core.AssignmentGroup')
#         first_feedbackset = group.feedbackset_set.first()
#         group.cached_data.refresh_from_db()
#         self.assertEqual(group.cached_data.last_feedbackset, first_feedbackset)
#         self.assertEqual(group.cached_data.first_feedbackset, first_feedbackset)
#         self.assertEqual(group.cached_data.last_published_feedbackset, None)
#
#     def test_first_feedbackset(self):
#         group = mommy.make('core.AssignmentGroup')
#         first_feedbackset = group.feedbackset_set.first()
#         mommy.make('devilry_group.FeedbackSet',
#                    group=group,
#                    deadline_datetime=ACTIVE_PERIOD_START)
#         mommy.make('devilry_group.FeedbackSet',
#                    group=group,
#                    deadline_datetime=ACTIVE_PERIOD_START + timedelta(days=2))
#         group.cached_data.refresh_from_db()
#         self.assertEqual(group.cached_data.first_feedbackset, first_feedbackset)
#
#     def test_last_feedbackset(self):
#         group = mommy.make('core.AssignmentGroup')
#         mommy.make('devilry_group.FeedbackSet',
#                    group=group,
#                    deadline_datetime=ACTIVE_PERIOD_START)
#         last_feedbackset = mommy.make('devilry_group.FeedbackSet',
#                                       group=group,
#                                       deadline_datetime=ACTIVE_PERIOD_START + timedelta(days=2))
#         group.cached_data.refresh_from_db()
#         self.assertEqual(group.cached_data.last_feedbackset, last_feedbackset)
#
#     def test_last_published_feedbackset_none(self):
#         group = mommy.make('core.AssignmentGroup')
#         mommy.make('devilry_group.FeedbackSet',
#                    group=group,
#                    deadline_datetime=ACTIVE_PERIOD_START)
#         group.cached_data.refresh_from_db()
#         self.assertEqual(group.cached_data.last_published_feedbackset, None)
#
#     def test_last_published_feedbackset_simple(self):
#         group = mommy.make('core.AssignmentGroup')
#         last_published_feedbackset = mommy.make(
#             'devilry_group.FeedbackSet',
#             group=group,
#             grading_published_datetime=ACTIVE_PERIOD_START,
#             deadline_datetime=ACTIVE_PERIOD_START)
#         group.cached_data.refresh_from_db()
#         self.assertEqual(group.cached_data.last_published_feedbackset,
#                          last_published_feedbackset)
#
#     def test_last_published_feedbackset_multiple(self):
#         group = mommy.make('core.AssignmentGroup')
#         mommy.make(
#             'devilry_group.FeedbackSet',
#             group=group,
#             grading_published_datetime=ACTIVE_PERIOD_START,
#             deadline_datetime=ACTIVE_PERIOD_START)
#         last_published_feedbackset = mommy.make(
#             'devilry_group.FeedbackSet',
#             group=group,
#             grading_published_datetime=ACTIVE_PERIOD_START,
#             deadline_datetime=ACTIVE_PERIOD_START + timedelta(days=2))
#         group.cached_data.refresh_from_db()
#         self.assertEqual(group.cached_data.last_published_feedbackset,
#                          last_published_feedbackset)
#
#     def test_last_published_feedbackset_ignore_unpublished(self):
#         group = mommy.make('core.AssignmentGroup')
#         last_published_feedbackset = mommy.make(
#             'devilry_group.FeedbackSet',
#             group=group,
#             grading_published_datetime=ACTIVE_PERIOD_START,
#             deadline_datetime=ACTIVE_PERIOD_START)
#         mommy.make(
#             'devilry_group.FeedbackSet',
#             group=group,
#             deadline_datetime=ACTIVE_PERIOD_START + timedelta(days=2))
#         group.cached_data.refresh_from_db()
#         self.assertEqual(group.cached_data.last_published_feedbackset,
#                          last_published_feedbackset)
#
    # def test_last_published_feedbackset_update_to(self):
    #     group = mommy.make('core.AssignmentGroup')
    #     feedbackset1 = group.feedbackset_set.first()
    #     feedbackset2 = mommy.make(
    #         'devilry_group.FeedbackSet',
    #         group=group,
    #         grading_published_datetime=ACTIVE_PERIOD_START,
    #         deadline_datetime=ACTIVE_PERIOD_START)
    #     group.cached_data.refresh_from_db()
        # self.assertEqual(group.cached_data.last_published_feedbackset,
        #                  last_published_feedbackset)

    # def test_create_published_feedbackset(self):
    #     feedbackset = mommy.make('devilry_group.FeedbackSet',
    #                              grading_published_datetime=timezone.now())
    #     cached_data = AssignmentGroupCachedData.objects.get(group=feedbackset.group)
    #     self.assertEqual(feedbackset, cached_data.last_published_feedbackset)
    #
    # def test_update_feedbackset_to_published_sanity(self):
    #     feedbackset = mommy.make('devilry_group.FeedbackSet', grading_published_datetime=None)
    #     feedbackset.grading_published_datetime = timezone.now()
    #     feedbackset.save()
    #     cached_data = AssignmentGroupCachedData.objects.get(group=feedbackset.group)
    #     self.assertEqual(feedbackset, cached_data.last_published_feedbackset)
    #
    # def test_update_feedbackset_to_unpublished_sanity(self):
    #     feedbackset = mommy.make('devilry_group.FeedbackSet', grading_published_datetime=timezone.now())
    #     feedbackset.grading_published_datetime = None
    #     feedbackset.save()
    #     cached_data = AssignmentGroupCachedData.objects.get(group=feedbackset.group)
    #     self.assertIsNone(cached_data.last_published_feedbackset)
    #
    # def test_feedbackset_count_insert(self):
    #     testgroup = mommy.make('core.AssignmentGroup')
    #     testgroup.cached_data.refresh_from_db()
    #     self.assertEqual(testgroup.cached_data.feedbackset_count, 1)
    #     mommy.make('devilry_group.FeedbackSet', group=testgroup)
    #     testgroup.cached_data.refresh_from_db()
    #     self.assertEqual(testgroup.cached_data.feedbackset_count, 2)

    # def test_feedbackset_count_delete(self):
    #     testgroup = mommy.make('core.AssignmentGroup')
    #     feedbackset2 = mommy.make('devilry_group.FeedbackSet', group=testgroup)
    #     testgroup.cached_data.refresh_from_db()
    #     self.assertEqual(testgroup.cached_data.feedbackset_count, 2)
    #     feedbackset2.delete()
    #     testgroup.refresh_from_db()
    #     testgroup.cached_data.refresh_from_db()
    #     print(AssignmentGroupCachedData.objects.all())
    #     self.assertEqual(testgroup.cached_data.feedbackset_count, 1)


# class TestAssignmentGroupTriggers(test.TestCase):
#
#     def setUp(self):
#         AssignmentGroupDbCacheCustomSql().initialize()
#
#     def test_create_group_creates_feedbackset_sanity(self):
#         group = mommy.make('core.AssignmentGroup')
#         autocreated_feedbackset = group.feedbackset_set.first()
#         self.assertIsNotNone(autocreated_feedbackset)
#         self.assertEqual(FeedbackSet.FEEDBACKSET_TYPE_FIRST_ATTEMPT, autocreated_feedbackset.feedbackset_type)
#
#     def test_create_group_creates_feedbackset_created_datetime_in_correct_timezone(self):
#         # NOTE: We add 60 sec to before and after, because Django and postgres servers
#         #       can be a bit out of sync with each other, and the important thing here
#         #       is that the timestamp is somewhat correct (not in the wrong timezone).
#         before = timezone.now() - timedelta(seconds=60)
#         group = mommy.make('core.AssignmentGroup')
#         after = timezone.now() + timedelta(seconds=60)
#         autocreated_feedbackset = group.feedbackset_set.first()
#         self.assertTrue(autocreated_feedbackset.created_datetime >= before)
#         self.assertTrue(autocreated_feedbackset.created_datetime <= after)
#
#
# class TestGroupCommentTriggers(test.TestCase):
#
#     def setUp(self):
#         AssignmentGroupDbCacheCustomSql().initialize()
#
#     def test_create_groupcomment_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(
#             group=testgroup)
#         mommy.make('devilry_group.GroupComment',
#                    feedback_set=feedbackset,
#                    comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                    user_role=GroupComment.USER_ROLE_STUDENT,
#                    visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         mommy.make('devilry_group.GroupComment',
#                    feedback_set=feedbackset,
#                    comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                    user_role=GroupComment.USER_ROLE_EXAMINER,
#                    visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         mommy.make('devilry_group.GroupComment',
#                    feedback_set=feedbackset,
#                    comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                    user_role=GroupComment.USER_ROLE_ADMIN,
#                    visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         self.assertEqual(3, testgroup.cached_data.public_total_comment_count)
#
#     def test_delete_groupcomment_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(
#             group=testgroup)
#         comment1 = mommy.make('devilry_group.GroupComment',
#                               feedback_set=feedbackset,
#                               comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                               user_role=GroupComment.USER_ROLE_STUDENT,
#                               visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         comment2 = mommy.make('devilry_group.GroupComment',
#                               feedback_set=feedbackset,
#                               comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                               user_role=GroupComment.USER_ROLE_EXAMINER,
#                               visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         comment3 = mommy.make('devilry_group.GroupComment',
#                               feedback_set=feedbackset,
#                               comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                               user_role=GroupComment.USER_ROLE_ADMIN,
#                               visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         comment1.delete()
#         comment2.delete()
#         comment3.delete()
#         self.assertEqual(0, testgroup.cached_data.public_total_comment_count)
#
#     def test_create_groupcomment_student_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(
#             group=testgroup)
#         mommy.make('devilry_group.GroupComment',
#                    feedback_set=feedbackset,
#                    comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                    user_role=GroupComment.USER_ROLE_STUDENT,
#                    visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         self.assertEqual(1, testgroup.cached_data.public_student_comment_count)
#
#     def test_delete_groupcomment_student_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(
#             group=testgroup)
#         comment1 = mommy.make('devilry_group.GroupComment',
#                               feedback_set=feedbackset,
#                               comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                               user_role=GroupComment.USER_ROLE_STUDENT,
#                               visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         comment1.delete()
#         self.assertEqual(0, testgroup.cached_data.public_student_comment_count)
#
#     def test_create_groupcomment_examiner_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(
#             group=testgroup)
#         mommy.make('devilry_group.GroupComment',
#                    feedback_set=feedbackset,
#                    comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                    user_role=GroupComment.USER_ROLE_EXAMINER,
#                    visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         self.assertEqual(1, testgroup.cached_data.public_examiner_comment_count)
#
#     def test_delete_groupcomment_examiner_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(
#             group=testgroup)
#         comment1 = mommy.make('devilry_group.GroupComment',
#                               feedback_set=feedbackset,
#                               comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                               user_role=GroupComment.USER_ROLE_EXAMINER,
#                               visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         comment1.delete()
#         self.assertEqual(0, testgroup.cached_data.public_examiner_comment_count)
#
#     def test_create_groupcomment_admin_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(
#             group=testgroup)
#         mommy.make('devilry_group.GroupComment',
#                    feedback_set=feedbackset,
#                    comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                    user_role=GroupComment.USER_ROLE_ADMIN,
#                    visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         self.assertEqual(1, testgroup.cached_data.public_admin_comment_count)
#
#     def test_delete_groupcomment_admin_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(
#             group=testgroup)
#         comment1 = mommy.make('devilry_group.GroupComment',
#                               feedback_set=feedbackset,
#                               comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                               user_role=GroupComment.USER_ROLE_ADMIN,
#                               visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         comment1.delete()
#         self.assertEqual(0, testgroup.cached_data.public_admin_comment_count)
#
#     def test_groupcomment_count_with_imageannotationcomment(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(
#             group=testgroup)
#         mommy.make('devilry_comment.CommentFile',
#                    comment=mommy.make('devilry_group.GroupComment',
#                                       feedback_set=feedbackset,
#                                       comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                                       user_role=GroupComment.USER_ROLE_STUDENT,
#                                       visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE))
#         testcomment = mommy.make('devilry_group.ImageAnnotationComment',
#                                  feedback_set=feedbackset,
#                                  comment_type=ImageAnnotationComment.COMMENT_TYPE_IMAGEANNOTATION,
#                                  user_role=ImageAnnotationComment.USER_ROLE_STUDENT,
#                                  visibility=ImageAnnotationComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         mommy.make('devilry_comment.CommentFile', comment=testcomment)
#         self.assertEqual(1, testgroup.cached_data.public_student_comment_count)
#         self.assertEqual(1, testgroup.cached_data.public_student_imageannotationcomment_count)
#
#
# class TestImageAnnotationCommentTriggers(test.TestCase):
#
#     def setUp(self):
#         AssignmentGroupDbCacheCustomSql().initialize()
#
#     def test_create_imageannotationcomment_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(
#             group=testgroup)
#         mommy.make('devilry_group.ImageAnnotationComment',
#                    feedback_set=feedbackset,
#                    comment_type=ImageAnnotationComment.COMMENT_TYPE_IMAGEANNOTATION,
#                    user_role=ImageAnnotationComment.USER_ROLE_STUDENT,
#                    visibility=ImageAnnotationComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         mommy.make('devilry_group.ImageAnnotationComment',
#                    feedback_set=feedbackset,
#                    comment_type=ImageAnnotationComment.COMMENT_TYPE_IMAGEANNOTATION,
#                    user_role=ImageAnnotationComment.USER_ROLE_EXAMINER,
#                    visibility=ImageAnnotationComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         mommy.make('devilry_group.ImageAnnotationComment',
#                    feedback_set=feedbackset,
#                    comment_type=ImageAnnotationComment.COMMENT_TYPE_IMAGEANNOTATION,
#                    user_role=ImageAnnotationComment.USER_ROLE_ADMIN,
#                    visibility=ImageAnnotationComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         self.assertEqual(3, testgroup.cached_data.public_total_imageannotationcomment_count)
#
#     def test_delete_imageannotationcomment_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(
#             group=testgroup)
#         comment1 = mommy.make('devilry_group.ImageAnnotationComment',
#                               feedback_set=feedbackset,
#                               comment_type=ImageAnnotationComment.COMMENT_TYPE_IMAGEANNOTATION,
#                               user_role=ImageAnnotationComment.USER_ROLE_STUDENT,
#                               visibility=ImageAnnotationComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         comment2 = mommy.make('devilry_group.ImageAnnotationComment',
#                               feedback_set=feedbackset,
#                               comment_type=ImageAnnotationComment.COMMENT_TYPE_IMAGEANNOTATION,
#                               user_role=ImageAnnotationComment.USER_ROLE_EXAMINER,
#                               visibility=ImageAnnotationComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         comment3 = mommy.make('devilry_group.ImageAnnotationComment',
#                               feedback_set=feedbackset,
#                               comment_type=ImageAnnotationComment.COMMENT_TYPE_IMAGEANNOTATION,
#                               user_role=ImageAnnotationComment.USER_ROLE_ADMIN,
#                               visibility=ImageAnnotationComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         comment1.delete()
#         comment2.delete()
#         comment3.delete()
#         self.assertEqual(0, testgroup.cached_data.public_total_imageannotationcomment_count)
#
#     def test_create_imageannotationcomment_student_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(
#             group=testgroup)
#         mommy.make('devilry_group.ImageAnnotationComment',
#                    feedback_set=feedbackset,
#                    comment_type=ImageAnnotationComment.COMMENT_TYPE_IMAGEANNOTATION,
#                    user_role=ImageAnnotationComment.USER_ROLE_STUDENT,
#                    visibility=ImageAnnotationComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         self.assertEqual(1, testgroup.cached_data.public_student_imageannotationcomment_count)
#
#     def test_delete_imageannotationcomment_student_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(
#             group=testgroup)
#         comment1 = mommy.make('devilry_group.ImageAnnotationComment',
#                               feedback_set=feedbackset,
#                               comment_type=ImageAnnotationComment.COMMENT_TYPE_IMAGEANNOTATION,
#                               user_role=ImageAnnotationComment.USER_ROLE_STUDENT,
#                               visibility=ImageAnnotationComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         comment1.delete()
#         self.assertEqual(0, testgroup.cached_data.public_student_imageannotationcomment_count)
#
#     def test_create_imageannotationcomment_examiner_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(
#             group=testgroup)
#         mommy.make('devilry_group.ImageAnnotationComment',
#                    feedback_set=feedbackset,
#                    comment_type=ImageAnnotationComment.COMMENT_TYPE_IMAGEANNOTATION,
#                    user_role=ImageAnnotationComment.USER_ROLE_EXAMINER,
#                    visibility=ImageAnnotationComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         self.assertEqual(1, testgroup.cached_data.public_examiner_imageannotationcomment_count)
#
#     def test_delete_imageannotationcomment_examiner_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(
#             group=testgroup)
#         comment1 = mommy.make('devilry_group.ImageAnnotationComment',
#                               feedback_set=feedbackset,
#                               comment_type=ImageAnnotationComment.COMMENT_TYPE_IMAGEANNOTATION,
#                               user_role=ImageAnnotationComment.USER_ROLE_EXAMINER,
#                               visibility=ImageAnnotationComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         comment1.delete()
#         self.assertEqual(0, testgroup.cached_data.public_examiner_imageannotationcomment_count)
#
#     def test_create_imageannotationcomment_admin_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(
#             group=testgroup)
#         mommy.make('devilry_group.ImageAnnotationComment',
#                    feedback_set=feedbackset,
#                    comment_type=ImageAnnotationComment.COMMENT_TYPE_IMAGEANNOTATION,
#                    user_role=ImageAnnotationComment.USER_ROLE_ADMIN,
#                    visibility=ImageAnnotationComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         self.assertEqual(1, testgroup.cached_data.public_admin_imageannotationcomment_count)
#
#     def test_delete_imageannotationcomment_admin_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(
#             group=testgroup)
#         comment1 = mommy.make('devilry_group.ImageAnnotationComment',
#                               feedback_set=feedbackset,
#                               comment_type=ImageAnnotationComment.COMMENT_TYPE_IMAGEANNOTATION,
#                               user_role=ImageAnnotationComment.USER_ROLE_ADMIN,
#                               visibility=ImageAnnotationComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         comment1.delete()
#         self.assertEqual(0, testgroup.cached_data.public_admin_imageannotationcomment_count)
#
#
# class TestCommentFileTriggers(test.TestCase):
#
#     def setUp(self):
#         AssignmentGroupDbCacheCustomSql().initialize()
#
#     def test_create_commentfile_total_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(group=testgroup)
#         testcomment1 = mommy.make('devilry_group.GroupComment',
#                                   feedback_set=feedbackset,
#                                   comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                                   user_role=GroupComment.USER_ROLE_STUDENT,
#                                   visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         mommy.make('devilry_comment.CommentFile', comment=testcomment1)
#         testcomment2 = mommy.make('devilry_group.GroupComment',
#                                   feedback_set=feedbackset,
#                                   comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                                   user_role=GroupComment.USER_ROLE_EXAMINER,
#                                   visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         mommy.make('devilry_comment.CommentFile', comment=testcomment2)
#         self.assertEqual(2, testgroup.cached_data.file_upload_count_total)
#
#     def test_delete_commentfile_total_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(group=testgroup)
#         testcomment1 = mommy.make('devilry_group.GroupComment',
#                                   feedback_set=feedbackset,
#                                   comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                                   user_role=GroupComment.USER_ROLE_STUDENT,
#                                   visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         commentfile1 = mommy.make('devilry_comment.CommentFile', comment=testcomment1)
#         testcomment2 = mommy.make('devilry_group.GroupComment',
#                                   feedback_set=feedbackset,
#                                   comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                                   user_role=GroupComment.USER_ROLE_EXAMINER,
#                                   visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         commentfile2 = mommy.make('devilry_comment.CommentFile', comment=testcomment2)
#         commentfile1.delete()
#         commentfile2.delete()
#         self.assertEqual(0, testgroup.cached_data.file_upload_count_total)
#
#     def test_create_commentfile_student_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(group=testgroup)
#         testcomment = mommy.make('devilry_group.GroupComment',
#                                  feedback_set=feedbackset,
#                                  comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                                  user_role=GroupComment.USER_ROLE_STUDENT,
#                                  visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         mommy.make('devilry_comment.CommentFile', comment=testcomment)
#         self.assertEqual(1, testgroup.cached_data.file_upload_count_student)
#
#     def test_delete_commentfile_student_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(group=testgroup)
#         testcomment = mommy.make('devilry_group.GroupComment',
#                                  feedback_set=feedbackset,
#                                  comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                                  user_role=GroupComment.USER_ROLE_STUDENT,
#                                  visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         commentfile = mommy.make('devilry_comment.CommentFile', comment=testcomment)
#         commentfile.delete()
#         self.assertEqual(0, testgroup.cached_data.file_upload_count_student)
#
#     def test_create_commentfile_examiner_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(group=testgroup)
#         testcomment = mommy.make('devilry_group.GroupComment',
#                                  feedback_set=feedbackset,
#                                  comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                                  user_role=GroupComment.USER_ROLE_EXAMINER,
#                                  visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         mommy.make('devilry_comment.CommentFile', comment=testcomment)
#         self.assertEqual(1, testgroup.cached_data.file_upload_count_examiner)
#
#     def test_delete_commentfile_examiner_gives_correct_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(group=testgroup)
#         testcomment = mommy.make('devilry_group.GroupComment',
#                                  feedback_set=feedbackset,
#                                  comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                                  user_role=GroupComment.USER_ROLE_EXAMINER,
#                                  visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         commentfile = mommy.make('devilry_comment.CommentFile', comment=testcomment)
#         commentfile.delete()
#         self.assertEqual(0, testgroup.cached_data.file_upload_count_examiner)
#
#
# class TestRecrateCacheData(test.TestCase):
#     def setUp(self):
#         AssignmentGroupDbCacheCustomSql().initialize()
#
#     def test_feedbackset_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         devilry_group_mommy_factories.feedbackset_first_attempt_published(group=testgroup)
#         devilry_group_mommy_factories.feedbackset_new_attempt_published(group=testgroup)
#         devilry_group_mommy_factories.feedbackset_new_attempt_unpublished(group=testgroup)
#         testgroup.refresh_from_db()
#         self.assertEqual(testgroup.cached_data.feedbackset_count, 3)
#         AssignmentGroupDbCacheCustomSql().recreate_data()
#         testgroup.refresh_from_db()
#         self.assertEqual(testgroup.cached_data.feedbackset_count, 3)
#
#     def test_public_total_comment_count(self):
#         testgroup = mommy.make('core.AssignmentGroup')
#         feedbackset = devilry_group_mommy_factories.feedbackset_first_attempt_published(group=testgroup)
#         testcomment1 = mommy.make('devilry_group.GroupComment',
#                                   feedback_set=feedbackset,
#                                   comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                                   user_role=GroupComment.USER_ROLE_STUDENT,
#                                   visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         mommy.make('devilry_comment.CommentFile', comment=testcomment1)
#         testcomment2 = mommy.make('devilry_group.GroupComment',
#                                   feedback_set=feedbackset,
#                                   comment_type=GroupComment.COMMENT_TYPE_GROUPCOMMENT,
#                                   user_role=GroupComment.USER_ROLE_EXAMINER,
#                                   visibility=GroupComment.VISIBILITY_VISIBLE_TO_EVERYONE)
#         mommy.make('devilry_comment.CommentFile', comment=testcomment2)
#         testgroup.refresh_from_db()
#         self.assertEqual(testgroup.cached_data.public_total_comment_count, 2)
#         AssignmentGroupDbCacheCustomSql().recreate_data()
#         testgroup.refresh_from_db()
#         self.assertEqual(testgroup.cached_data.public_total_comment_count, 2)
#
#
# class TimeExecution(object):
#     def __init__(self, label):
#         self.start_time = None
#         self.label = label
#
#     def __enter__(self):
#         self.start_time = datetime.now()
#
#     def __exit__(self, ttype, value, traceback):
#         end_time = datetime.now()
#         duration = (end_time - self.start_time).total_seconds()
#         print
#         print '{}: {}s'.format(self.label, duration)
#         print
#
#
# def _run_sql(sql):
#     cursor = connection.cursor()
#     cursor.execute(sql)
#
#
# def _remove_triggers():
#     _run_sql("""
#         DROP TRIGGER IF EXISTS devilry_dbcache_on_assignmentgroup_insert_trigger
#             ON core_assignmentgroup;
#         DROP TRIGGER IF EXISTS devilry_dbcache_on_feedbackset_insert_or_update_trigger
#             ON devilry_group_feedbackset;
#
#         DROP TRIGGER IF EXISTS devilry_dbcache_on_group_imageannotationcomment_trigger
#             ON devilry_group_imageannotationcomment;
#
#         DROP TRIGGER IF EXISTS devilry_dbcache_on_group_change_trigger
#             ON devilry_group_imageannotationcomment;
#     """)
#
#
# @unittest.skip('Bechmark - should just be enabled when debugging performance')
# class TestBenchMarkAssignmentGroupFileUploadCountTrigger(test.TestCase):
#
#     def setUp(self):
#         _remove_triggers()
#
#     def __create_distinct_comments(self, label):
#         assignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
#         group = mommy.make('core.AssignmentGroup', parentnode=assignment)
#         feedbackset = mommy.make('devilry_group.FeedbackSet', group=group)
#
#         examiner = mommy.make('core.Examiner',
#                               assignmentgroup=group,
#                               relatedexaminer__user=mommy.make(settings.AUTH_USER_MODEL))
#
#         mommy.make(GroupComment, user=examiner.relatedexaminer.user, feedback_set=feedbackset,
#                    user_role=GroupComment.USER_ROLE_ADMIN)
#         comment_student = mommy.make(GroupComment, user=examiner.relatedexaminer.user, feedback_set=feedbackset,
#                                      user_role=GroupComment.USER_ROLE_STUDENT)
#         comment_examiner = mommy.make(GroupComment, user=examiner.relatedexaminer.user, feedback_set=feedbackset,
#                                       user_role=GroupComment.USER_ROLE_EXAMINER)
#
#         count = 1000
#         with TimeExecution('{} ({})'.format(label, count)):
#             for x in range(count):
#                 student_file = mommy.make(CommentFile, comment=comment_student)
#                 student_file.file.save('testfile.txt', ContentFile('test'))
#                 examiner_file = mommy.make(CommentFile, comment=comment_examiner)
#                 examiner_file.file.save('testfile.txt', ContentFile('test'))
#                 # student_file.delete()
#
#                 # f or c in comments:
#                 #     c.save()
#
#                 # for c in comments:
#                 #     c.delete()
#                 #
#                 # cached_data = AssignmentGroupCachedData.objects.get(group=group)
#                 # print "feedbackset_count:", cached_data.feedbackset_count
#                 # print "public_total_comment_count:", cached_data.public_total_comment_count
#                 # print "public_student_comment_count:", cached_data.public_student_comment_count
#                 # print "public_examiner_comment_count:", cached_data.public_examiner_comment_count
#                 # print "public_admin_comment_count:", cached_data.public_admin_comment_count
#                 #
#                 #
#                 # print "file_upload_count_total:", cached_data.file_upload_count_total
#                 # print "file_upload_count_student:", cached_data.file_upload_count_student
#                 # print "file_upload_count_examiner:", cached_data.file_upload_count_examiner
#
#     def test_create_in_distinct_groups_without_triggers(self):
#         self.__create_distinct_comments('file upload: no triggers')
#
#     def test_create_in_distinct_groups_with_triggers(self):
#         AssignmentGroupDbCacheCustomSql().initialize()
#         self.__create_distinct_comments('file upload: with triggers')
#
#
# @unittest.skip('Bechmark - should just be enabled when debugging performance')
# class TestBenchMarkFeedbackSetTrigger(test.TestCase):
#
#     def setUp(self):
#         _remove_triggers()
#
#     def __create_in_distinct_groups_feedbacksets(self, label):
#         count = 10000
#         assignment = mommy.make('core.Assignment')
#         created_by = mommy.make(settings.AUTH_USER_MODEL)
#
#         groups = []
#         for x in range(count):
#             groups.append(mommy.prepare('core.AssignmentGroup', parentnode=assignment))
#         AssignmentGroup.objects.bulk_create(groups)
#
#         feedbacksets = []
#         for group in AssignmentGroup.objects.filter(parentnode=assignment):
#             feedbackset = mommy.prepare(FeedbackSet, group=group, created_by=created_by, is_last_in_group=None)
#             feedbacksets.append(feedbackset)
#
#         with TimeExecution('{} ({})'.format(label, count)):
#             FeedbackSet.objects.bulk_create(feedbacksets)
#
#     def test_create_feedbacksets_in_distinct_groups_without_triggers(self):
#         self.__create_in_distinct_groups_feedbacksets('feedbacksets distinct groups: no triggers')
#
#     def test_create_feedbacksets_in_distinct_groups_with_triggers(self):
#         AssignmentGroupDbCacheCustomSql().initialize()
#         self.__create_in_distinct_groups_feedbacksets('feedbacksets distinct groups: with triggers')
#
#     def __create_in_same_group_feedbacksets(self, label):
#         count = 1000
#         assignment = mommy.make('core.Assignment')
#         created_by = mommy.make(settings.AUTH_USER_MODEL)
#         group = mommy.make('core.AssignmentGroup', parentnode=assignment)
#
#         feedbacksets = []
#         for x in range(count):
#             feedbackset = mommy.prepare(FeedbackSet, group=group, created_by=created_by, is_last_in_group=None)
#             feedbacksets.append(feedbackset)
#
#         with TimeExecution('{} ({})'.format(label, count)):
#             FeedbackSet.objects.bulk_create(feedbacksets)
#
#     def test_create_feedbacksets_in_same_group_without_triggers(self):
#         self.__create_in_same_group_feedbacksets('feedbacksets same group: no triggers')
#
#     def test_create_feedbacksets_in_same_group_with_triggers(self):
#         AssignmentGroupDbCacheCustomSql().initialize()
#         # This should have some overhead because we need to UPDATE the AssignmentGroupCachedData
#         # for each INSERT
#         self.__create_in_same_group_feedbacksets('feedbacksets same group: with triggers')
#
#
# @unittest.skip('Bechmark - should just be enabled when debugging performance')
# class TestBenchMarkAssignmentGroupTrigger(test.TestCase):
#     def setUp(self):
#         _remove_triggers()
#
#     def __create_distinct_groups(self, label):
#         count = 10000
#         assignment = mommy.make('core.Assignment')
#         groups = []
#         for x in range(count):
#             groups.append(mommy.prepare('core.AssignmentGroup', parentnode=assignment))
#
#         with TimeExecution('{} ({})'.format(label, count)):
#             AssignmentGroup.objects.bulk_create(groups)
#
#     def test_create_in_distinct_groups_without_triggers(self):
#         self.__create_distinct_groups('assignment groups: no triggers')
#
#     def test_create_in_distinct_groups_with_triggers(self):
#         AssignmentGroupDbCacheCustomSql().initialize()
#         self.__create_distinct_groups('assignment groups: with triggers')
#
#
# @unittest.skip('Bechmark - should just be enabled when debugging performance')
# class TestBenchMarkAssignmentGroupCommentCountTrigger(test.TestCase):
#     def setUp(self):
#         _remove_triggers()
#
#     def __create_distinct_comments(self, label):
#         assignment = mommy.make_recipe('devilry.apps.core.assignment_activeperiod_start')
#         group = mommy.make('core.AssignmentGroup', parentnode=assignment)
#         feedbackset = mommy.make('devilry_group.FeedbackSet', group=group)
#
#         examiner = mommy.make('core.Examiner',
#                               assignmentgroup=group,
#                               relatedexaminer__user=mommy.make(settings.AUTH_USER_MODEL))
#
#         count = 100
#         comments = []
#         for x in range(count):
#             comments.append(mommy.prepare(GroupComment, user=examiner.relatedexaminer.user, feedback_set=feedbackset,
#                                           user_role=GroupComment.USER_ROLE_ADMIN))
#             comments.append(mommy.prepare(GroupComment, user=examiner.relatedexaminer.user, feedback_set=feedbackset,
#                                           user_role=GroupComment.USER_ROLE_STUDENT))
#             comments.append(mommy.prepare(GroupComment, user=examiner.relatedexaminer.user, feedback_set=feedbackset,
#                                           user_role=GroupComment.USER_ROLE_EXAMINER))
#
#         with TimeExecution('{} ({})'.format(label, count)):
#             for c in comments:
#                 c.save()
#
#                 # for c in comments:
#                 #    c.delete()
#                 #
#         return group
#
#     def test_create_in_distinct_groups_without_triggers(self):
#         self.__create_distinct_comments('assignment groups comments: no triggers')
#
#     def test_create_in_distinct_groups_with_triggers(self):
#         AssignmentGroupDbCacheCustomSql().initialize()
#         group = self.__create_distinct_comments('assignment groups comments: with triggers')
#         cached_data = AssignmentGroupCachedData.objects.get(group=group)
#         print "feedbackset_count:", cached_data.feedbackset_count
#         print "public_total_comment_count:", cached_data.public_total_comment_count
#         print "public_student_comment_count:", cached_data.public_student_comment_count
#         print "public_examiner_comment_count:", cached_data.public_examiner_comment_count
#         print "public_admin_comment_count:", cached_data.public_admin_comment_count
