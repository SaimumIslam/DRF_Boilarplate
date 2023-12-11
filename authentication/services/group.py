from base.services.base import BaseService

from ..repositories.group import GroupRepository


class GroupService(BaseService):
    def __init__(self):
        super().__init__(GroupRepository)

    def post_migration_create(self):
        self.repository.post_migration_create()

    def add_user_by_group_name__user(self, group_name, user):
        self.repository.add_user_by_group_name__user(group_name, user)

    def add_permission_by_group_name(self, permission, group_name):
        self.repository.add_permission_by_group_name(permission, group_name)
