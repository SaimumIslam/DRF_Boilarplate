from django.db.models import Q
from django.contrib.auth.models import Permission

from base.repositories.base import BaseRepository


class PermissionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Permission)

    def get_by_name(self, name):
        try:
            return self.model.objects.get(name=name)
        except self.model.DoesNotExist:
            return None

    def add_user_by_codename(self, user, code_name):
        instance = self.get_by_attr(name=code_name)
        if instance:
            instance.user_set.add(user)

    def get_group_permissions_by_user(self, user):
        return self.queryset.filter(group__user=user)

    def get_permissions_by_user(self, user):
        or_filters = Q(group__user=user) | Q(user=user)
        return self.queryset.filter(or_filters).distinct()

    def has_permissions_by_user(self, user):
        or_filters = Q(group__user=user) | Q(user=user)
        return self.queryset.filter(or_filters).exists()

    def has_permissions_by_user__codename(self, user, codename):
        or_filters = Q(group__user=user) | Q(user=user)
        return self.queryset.filter(or_filters, codename=codename).exists()
