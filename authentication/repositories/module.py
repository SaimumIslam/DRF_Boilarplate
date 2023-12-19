from base.repositories.base import BaseRepository
from authentication.models import Module


class ModuleRepository(BaseRepository):
    def __init__(self):
        super().__init__(Module)
