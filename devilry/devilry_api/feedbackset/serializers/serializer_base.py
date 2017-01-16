from rest_framework import serializers

from devilry.apps.core.models import Examiner
from devilry.devilry_group.models import FeedbackSet


class DeadlineDatetime(serializers.DateTimeField):

    def get_attribute(self, instance):
        """
        returns the current deadline of the feedbackset

        Args:
            instance: :obj:`devilry_group.Feedbackset`

        Returns:
            :method:`devilry_group.Feedbackset.current_deadline`
        """
        return instance.current_deadline()

class BaseFeedbacksetSerializer(serializers.Serializer):
    FEEDBACKSET_CHOICES = FeedbackSet.FEEDBACKSET_TYPE_CHOICES

    #: Id of feedbackset.
    id = serializers.IntegerField(required=False, read_only=True)

    #: Id of related group.
    group_id = serializers.IntegerField(required=True)

    #: Feedbackset created datetime.
    created_datetime = serializers.DateTimeField(read_only=True)

    #: Feedbackset type
    feedbackset_type = serializers.ChoiceField(choices=FEEDBACKSET_CHOICES, required=True)

    #: Feedbackset deadline datetime
    deadline_datetime = DeadlineDatetime(required=True)

    #: Creator of feedbackset full name
    created_by_fullname = serializers.SerializerMethodField()

    @property
    def devilry_role(self):
        """
        Override this to return 'student'
                                'examiner',
                                'periodadmin',
                                'subjectadmin' or
                                'departmentadmin'.

        Raises:
            :class:`NotImplementedError`
        """
        raise NotImplementedError("Please set devilry_role example: devilry_role = 'student'")

    def get_created_by_fullname(self, instance):
        """
        Gets full name of the examiner or anonymized name.

        Args:
            instance: :obj:`~devilry_group.Feedbackset`

        Returns:
            :attr:`devilry_account.User.fullname` or anonymized name (str)
        """
        anonymous = instance.group.parentnode. \
            examiners_must_be_anonymized_for_devilryrole(self.devilry_role)
        try:
            examiner = Examiner.objects.get(relatedexaminer__user=instance.created_by,
                                            assignmentgroup=instance.group)
        except Examiner.DoesNotExist:
            return None
        if anonymous:
            return examiner.get_anonymous_name()
        return examiner.relatedexaminer.user.fullname
