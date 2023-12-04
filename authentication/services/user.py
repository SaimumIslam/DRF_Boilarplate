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
