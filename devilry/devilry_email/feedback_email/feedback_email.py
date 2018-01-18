from django.utils.translation import ugettext_lazy

import django_rq
from django_cradmin.crinstance import reverse_cradmin_url
from devilry.utils.devilry_email import send_templated_message
from devilry.devilry_email.utils import get_student_users_in_group


def send_feedback_email(feedback_set, points, domain_url_start, subject):
    """
    Send a feedback mail to all students in and :class:`~.devilry.apps.core.models.AssignmentGroup` for
    a :class:`~.devilry.devilry_group.models.FeedbackSet`.

    Args:
        feedback_set: The feedback_set that was corrected.
        points: Points given on the ``FeedbackSet``.
        user: The user that corrected the ``FeedbackSet``.
        subject: The email subject.
    """
    # assignment = feedback_set.group.parentnode
    # subject = ugettext_lazy('Feedback for %(assignment_name)s') % {'assignment_name': assignment.long_name}
    template_name = 'devilry_email/feedback_email/assignment_feedback_student.txt'

    # Build absolute url
    domain_url_start = domain_url_start.rstrip('/')
    absolute_url = '{}{}'.format(
        domain_url_start,
        reverse_cradmin_url(instanceid='devilry_group_student', appname='feedbackfeed', roleid=feedback_set.group_id)
    )
    student_users = list(get_student_users_in_group(feedback_set.group))
    send_templated_message(subject, template_name, {
        'assignment': feedback_set.group.parentnode,
        'devilryrole': 'student',
        'points': points,
        'deadline_datetime': feedback_set.deadline_datetime,
        'corrected_datetime': feedback_set.grading_published_datetime,
        'url': absolute_url
    }, *student_users)


def send_feedback_edited_email(**kwargs):
    """
    Send feedback updated email. With customized subject for edited feedback.
    """
    assignment = kwargs['feedback_set'].group.parentnode
    kwargs.update({
        'subject': ugettext_lazy('Feedback updated for %(assignment_name)s') % {'assignment_name': assignment.long_name}
    })
    send_feedback_email(**kwargs)


def send_feedback_created_email(**kwargs):
    """
    Send feedback created email. With customized subject for newly published feedback.
    """
    assignment = kwargs['feedback_set'].group.parentnode
    kwargs.update({
        'subject': ugettext_lazy('Feedback for %(assignment_name)s') % {'assignment_name': assignment.long_name}
    })
    send_feedback_email(**kwargs)


def bulk_feedback_mail(feedbackset_id_list, domain_url_start):
    """
    Starts an RQ task that sends a mail users in  a group for FeedbackSet.

    Args:
        feedbackset_id_list: A list of :class:`~.devilry.devilry_group.models.FeedbackSet`
        request: A ``DjangoHttpRequest`` object needed to build an absolute URI.
    """
    from devilry.devilry_group.models import FeedbackSet
    feedbackset_queryset = FeedbackSet.objects\
        .select_related('group', 'group__parentnode', 'group__parentnode__parentnode')\
        .filter(id__in=feedbackset_id_list)
    for feedback_set in feedbackset_queryset:
        send_feedback_created_email(
            feedback_set=feedback_set,
            points=feedback_set.grading_points,
            domain_url_start=domain_url_start
        )


def bulk_send_email(**kwargs):
    """
    Queues bulk sending of emails to students.

    This method only handles the queueing, and calls :func:`.bulk_feedback_mail` as the RQ task.

    Args:
        **kwargs: Arguments required by :func:`.bulk_feedback_mail`.
    """
    queue = django_rq.get_queue(name='email')
    queue.enqueue(bulk_feedback_mail, **kwargs)