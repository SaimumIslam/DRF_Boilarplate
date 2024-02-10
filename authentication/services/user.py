from base.services.base import BaseService

from ..repositories.user import UserRepository
from ..repositories.profile import ProfileRepository


class UserService(BaseService):
    def __init__(self):
        self.profile_repository = ProfileRepository()
        super().__init__(UserRepository)

    def post_save(self, user):
        self.profile_repository.create(user=user)

    def get_item_by_email(self, email):
        return self.repository.get_by_email(email)

    def add_permission_by_permission__user_id(self, permission, user_id):
        self.repository.add_permission_by_permission__user_id(permission, user_id)

    def remove_permission_by_permission__user_id(self, permission, user_id):
        self.repository.remove_permission_by_permission__user_id(permission, user_id)

    def add_restriction_by_restriction__user_id(self, permission, user_id):
        self.repository.add_restriction_by_restriction__user_id(permission, user_id)

    def remove_restriction_by_restriction__user_id(self, permission, user_id):
        self.repository.remove_restriction_by_restriction__user_id(permission, user_id)

    def add_group_by_group__user_id(self, group, user_id):
        self.repository.add_group_by_group__user_id(group, user_id)

    def remove_group_by_group__user_id(self, group, user_id):
        self.repository.remove_group_by_group__user_id(group, user_id)
