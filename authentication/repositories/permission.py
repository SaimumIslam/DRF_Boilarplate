from django.db.models import Q

from base.repositories.base import BaseRepository
from ..models import Permission


class PermissionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Permission)

    def get_group_permissions_by_group(self, group):
        return self.queryset.filter(group=group)

    def has_all_including_group_permissions_by_user__codename(self, user, codename):
        or_filters = Q(group__user=user) | Q(user=user)
        return self.queryset.filter(or_filters, codename=codename).exists()
