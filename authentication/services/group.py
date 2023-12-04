from base.services.base import BaseService

from ..repositories.group import GroupRepository


class GroupService(BaseService):
    def __init__(self):
        super().__init__(GroupRepository)

    def post_migration_create(self):
        self.repository.post_migration_create()

    def add_to_group_by_group_name__user(self, user, group_name):
        self.repository.add_to_group_by_group_name__user(user, group_name)
