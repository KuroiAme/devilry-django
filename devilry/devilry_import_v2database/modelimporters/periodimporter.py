import pprint

from django.contrib.auth import get_user_model

from devilry.apps.core.models import Subject, Period
from devilry.devilry_account import models as account_models
from devilry.devilry_import_v2database import modelimporter


class PeriodImporter(modelimporter.ModelImporter):
    def get_model_class(self):
        return Period

    def _create_permissiongroup_user(self, permission_group, user):
        permission_group_user = account_models.PermissionGroupUser(
            permissiongroup=permission_group,
            user=user
        )
        permission_group_user.full_clean()
        permission_group_user.save()
        return permission_group_user

    def _create_permissiongroup(self, name, admin_user_ids):
        admin_users_queryset = get_user_model().objects.filter(id__in=admin_user_ids)
        permission_group = account_models.PermissionGroup(
            grouptype=account_models.PermissionGroup.GROUPTYPE_PERIODADMIN,
            name='{} admins'.format(name)
        )
        permission_group.full_clean()
        permission_group.save()
        for admin_user in admin_users_queryset.all():
            self._create_permissiongroup_user(permission_group, admin_user)
        return permission_group

    def _create_period_permissiongroup(self, period, admin_user_ids):
        if len(admin_user_ids) > 0:
            permission_group = self._create_permissiongroup(
                name=period.short_name,
                admin_user_ids=admin_user_ids
            )
            period_permissiongroup = account_models.PeriodPermissionGroup(
                permissiongroup=permission_group,
                period=period
            )
            period_permissiongroup.full_clean()
            period_permissiongroup.save()

    def _get_subject_from_parentnode_id(self, id):
        try:
            subject = Subject.objects.get(id=id)
        except Subject.DoesNotExist:
            raise modelimporter.ModelImporterException('No Subject with id={} exists for imported Period'.format(id))
        return subject

    def _create_period_from_object_dict(self, object_dict):
        period = self.get_model_class()()
        self.patch_model_from_object_dict(
            model_object=period,
            object_dict=object_dict,
            attributes=[
                'pk',
                'long_name',
                'short_name',
                'start_time',
                'end_time',
            ]
        )
        period.parentnode = self._get_subject_from_parentnode_id(id=object_dict['fields']['parentnode'])
        period.full_clean()
        period.save()
        self._create_period_permissiongroup(period=period, admin_user_ids=object_dict['admin_user_ids'])
        self.log_create(model_object=period, data=object_dict)

    def import_models(self, fake=False):
        for object_dict in self.v2period_directoryparser.iterate_object_dicts():
            if fake:
                print('Would import: {}'.format(pprint.pformat(object_dict)))
            else:
                self._create_period_from_object_dict(object_dict=object_dict)

