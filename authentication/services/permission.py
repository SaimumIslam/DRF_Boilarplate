from base.services.base import BaseService

from ..repositories.permission import PermissionRepository


class PermissionService(BaseService):
    def __init__(self):
        super().__init__(PermissionRepository)

    def get_group_permissions_by_group(self, group):
        return self.repository.get_group_permissions_by_group(group)

    def has_permissions_by_user__codename(self, user, codename):
        return self.repository.has_permissions_by_user__codename(user, codename)

    def has_restrictions_by_user__codename(self, user, codename):
        return self.repository.has_restrictions_by_user__codename(user, codename)

    def has_api_permission_by_user__codename(self, user, codename):
        return self.repository.has_api_permission_by_user__codename(user, codename)
