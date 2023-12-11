from base.services.base import BaseService

from ..repositories.profile import ProfileRepository


class ProfileService(BaseService):
    def __init__(self):
        super().__init__(ProfileRepository)

    def get_items_by_keyword(self, keyword):
        return self.repository.get_items_by_keyword(keyword)
