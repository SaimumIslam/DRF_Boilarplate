from django.db.models import Q, Value, F
from django.db.models.functions import Concat

from base.repositories.base import BaseRepository

from ..models import User


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)
        self.queryset = self.model.objects.filter()

    def get_by_email(self, email):
        return self.queryset.filter(email=email).first()

    def add_permission_by_permission__user_id(self, permission, user_id):
        instance = self.get_by_attr(pk=user_id)
        if instance:
            instance.user_permissions.add(permission)

    def remove_permission_by_permission__user_id(self, permission, user_id):
        instance = self.get_by_attr(pk=user_id)
        if instance:
            instance.user_permissions.remove(permission)

    def add_restriction_by_restriction__user_id(self, restriction, user_id):
        instance = self.get_by_attr(pk=user_id)
        if instance:
            instance.user_restrictions.add(restriction)

    def remove_restriction_by_restriction__user_id(self, restriction, user_id):
        instance = self.get_by_attr(pk=user_id)
        if instance:
            instance.user_restrictions.remove(restriction)

    def add_group_by_group__user_id(self, group, user_id):
        instance = self.get_by_attr(pk=user_id)
        if instance:
            instance.groups.add(group)

    def remove_group_by_group__user_id(self, group, user_id):
        instance = self.get_by_attr(pk=user_id)
        if instance:
            instance.groups.remove(group)