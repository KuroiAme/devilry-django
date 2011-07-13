from ...simplified import simplified_modelapi, SimplifiedModelApi, PermissionDenied
from simplifiedmetabases import (SimplifiedSubjectMetaMixin, SimplifiedPeriodMetaMixin,
                                 SimplifiedAssignmentMetaMixin, SimplifiedAssignmentGroupMetaMixin,
                                 SimplifiedDeadlineMetaMixin, SimplifiedDeliveryMetaMixin,
                                 SimplifiedStaticFeedbackMetaMixin, SimplifiedFileMetaMetaMixin)


class PublishedWhereIsCandidateMixin(SimplifiedModelApi):
    """ Mixin class extended by all classes in the Simplified API for Student using the Simplified API """

    @classmethod
    def create_searchqryset(cls, user, **kwargs):
        """ Returns all objects of this type that matches arguments
        given in ``\*\*kwargs`` where ``user`` is a student.

        :param user: A django user object.
        :param \*\*kwargs: A dict containing search-parameters.
        :rtype: a django queryset
        """
        return cls._meta.model.published_where_is_candidate(user)

    @classmethod
    def read_authorize(cls, user, obj):
        """ Checks if the given ``user`` is an student in the given
        ``obj``, and raises ``PermissionDenied`` if not.

        :param user: A django user object.
        :param obj: An object of the type this method is used in.
        :throws PermissionDenied:
        """
        if not obj.published_where_is_candidate(user).filter(id=obj.id):
            raise PermissionDenied()


@simplified_modelapi
class SimplifiedFileMeta(PublishedWhereIsCandidateMixin, SimplifiedModelApi):
    """ Simplified wrapper for :class:`devilry.apps.core.models.FileMeta`. """
    class Meta(SimplifiedFileMetaMetaMixin):
        """ Defines what methods a Student can use on a FileMeta object using the Simplified API """
        methods = ['search', 'read', 'create']


@simplified_modelapi
class SimplifiedDeadline(PublishedWhereIsCandidateMixin):
    """ Simplified wrapper for :class:`devilry.apps.core.models.Deadline`. """
    class Meta(SimplifiedDeadlineMetaMixin):
        """ Defines what methods a Student can use on a Deadline object using the Simplified API """
        methods = ['search', 'read']


@simplified_modelapi
class SimplifiedStaticFeedback(PublishedWhereIsCandidateMixin, SimplifiedModelApi):
    """ Simplified wrapper for :class:`devilry.apps.core.models.StaticFeedback`. """
    class Meta(SimplifiedStaticFeedbackMetaMixin):
        """ Defines what methods a Student can use on a StaticFeedback object using the Simplified API """
        methods = ['search', 'read']


@simplified_modelapi
class SimplifiedDelivery(PublishedWhereIsCandidateMixin, SimplifiedModelApi):
    """ Simplified wrapper for :class:`devilry.apps.core.models.Delivery`. """
    class Meta(SimplifiedDeliveryMetaMixin):
        """ Defines what methods a Student can use on a Delivery object using the Simplified API """
        methods = ['search', 'read', 'delete']


@simplified_modelapi
class SimplifiedAssignmentGroup(PublishedWhereIsCandidateMixin, SimplifiedModelApi):
    """ Simplified wrapper for :class:`devilry.apps.core.models.AssignmentGroup`. """
    class Meta(SimplifiedAssignmentGroupMetaMixin):
        """ Defines what methods a Student can use on an AssignmentGroup object using the Simplified API """
        methods = ['search', 'read', 'create']


@simplified_modelapi
class SimplifiedAssignment(PublishedWhereIsCandidateMixin, SimplifiedModelApi):
    """ Simplified wrapper for :class:`devilry.apps.core.models.Assignment`. """
    class Meta(SimplifiedAssignmentMetaMixin):
        """ Defines what methods a Student can use on an Assignment object using the Simplified API """
        methods = ['search', 'read']


@simplified_modelapi
class SimplifiedPeriod(PublishedWhereIsCandidateMixin, SimplifiedModelApi):
    """ Simplified wrapper for :class:`devilry.apps.core.models.Period`. """
    class Meta(SimplifiedPeriodMetaMixin):
        """ Defines what methods a Student can use on a Period object using the Simplified API """
        methods = ['search', 'read']


@simplified_modelapi
class SimplifiedSubject(PublishedWhereIsCandidateMixin, SimplifiedModelApi):
    """ Simplified wrapper for :class:`devilry.apps.core.models.Subject`. """
    class Meta(SimplifiedSubjectMetaMixin):
        """ Defines what methods a Student can use on a Subject object using the Simplified API """
        methods = ['search', 'read']
