import bleach
from django import template
from django.utils.translation import ugettext_lazy as _
from devilry.utils import datetimeutils

register = template.Library()


@register.filter
def devilry_user_displayname(user):
    if not user:
        return ''
    return user.get_full_name()


@register.filter
def format_is_passing_grade(is_passing_grade):
    if is_passing_grade:
        return _('passed')
    else:
        return _('failed')


@register.filter
def devilry_feedback_shortformat(staticfeedback):
    if not staticfeedback:
        return ''
    if staticfeedback.grade in ('Passed', 'Failed'):
        return staticfeedback.grade
    else:
        return u'{} ({})'.format(
            staticfeedback.grade,
            format_is_passing_grade(staticfeedback.is_passing_grade))


@register.filter
def devilry_escape_html(html):
    """
    Escape all html in the given ``html``.
    """
    return bleach.clean(html)


@register.filter
def devilry_isoformat_datetime(datetimeobject):
    """
    Isoformat the given ``datetimeobject`` as ``YYYY-MM-DD hh:mm``.
    """
    return datetimeutils.isoformat_noseconds(datetimeobject)


@register.inclusion_tag('devilry_core/templatetags/single-candidate-long-displayname.django.html')
def devilry_single_candidate_long_displayname(assignment, candidate):
    """
    Returns the candidate wrapped in HTML formatting tags perfect for showing
    the user inline.

    Handles anonymization based on ``assignment.anonymizationmode``.

    Args:
        assignment: A :class:`devilry.apps.core.models.assignment.Assignment` object.
            The ``assignment`` should be the assignment where the candidate belongs.
        candidate: A :class:`devilry.apps.core.models.candidate.Candidate` object.
    """
    return {
        'assignment': assignment,
        'candidate': candidate,
    }
