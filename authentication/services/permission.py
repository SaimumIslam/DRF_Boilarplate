from base.services.base import BaseService

from ..repositories.permission import PermissionRepository


class PermissionService(BaseService):
    def __init__(self):
        super().__init__(PermissionRepository)

    def get_by_name(self, name):
        self.repository.get_by_name(name)

    def add_user_by_codename(self, user, code_name):
        self.repository.add_user_by_codename(user, code_name)

    def get_group_permissions_by_user(self, user):
        return self.repository.get_group_permissions_by_user(user)

    def get_permissions_by_user(self, user):
        return self.repository.get_permissions_by_user(user)

    def has_permissions_by_user(self, user):
        return self.repository.has_permissions_by_user(user)

    def has_permissions_by_user__codename(self, user, codename):
        return self.repository.has_permissions_by_user__codename(user, codename)
