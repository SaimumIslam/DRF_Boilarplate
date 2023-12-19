from base.services.base import BaseService
from authentication.repositories.module import ModuleRepository


class ModuleService(BaseService):
    def __init__(self):
        super().__init__(ModuleRepository)
