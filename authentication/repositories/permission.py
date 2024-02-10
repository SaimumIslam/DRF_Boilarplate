from django.db.models import Q

from base.repositories.base import BaseRepository
from ..models import Permission


class PermissionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Permission)

    def get_group_permissions_by_group(self, group):
        return self.queryset.filter(group=group)

    def has_permissions_by_user__codename(self, user, codename):
        return self.queryset.filter(user=user, codename=codename).exists()

    def has_restrictions_by_user__codename(self, user, codename):
        return self.queryset.filter(r_user=user, codename=codename).exists()

    def has_api_permission_by_user__codename(self, user, codename):
        or_filters = Q(group__user=user) | Q(user=user)

        return self.queryset.filter(or_filters, codename=codename).exists()
