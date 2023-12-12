from base.services.base import BaseService

from ..repositories.group import GroupRepository


class GroupService(BaseService):
    def __init__(self):
        super().__init__(GroupRepository)

    def post_migration_create(self):
        self.repository.post_migration_create()

    def add_permission_by_permission__group_id(self, permission, group_id):
        self.repository.add_permission_by_permission__group_id(permission, group_id)

    def remove_permission_by_permission__group_id(self, permission, group_id):
        self.repository.remove_permission_by_permission__group_id(permission, group_id)