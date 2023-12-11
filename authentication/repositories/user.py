from django.db.models import Q, Value, F
from django.db.models.functions import Concat

from base.repositories.base import BaseRepository

from ..models import User


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)
        self.queryset = self.model.objects.filter()

    def get_by_email(self, email):
        return self.queryset.filter(email=email).first()
