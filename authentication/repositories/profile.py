from django.db.models import Q, Value, F
from django.db.models.functions import Concat

from base.repositories.base import BaseRepository

from ..models import Profile


class ProfileRepository(BaseRepository):
    def __init__(self):
        super().__init__(Profile)

    def get_items_by_keyword(self, keyword, **kwargs):
        queryset = kwargs.get("queryset", self.queryset)
        if not keyword:
            return queryset

        or_filters = Q()
        or_filters = or_filters | \
                     Q(user__full_name__icontains=keyword) | \
                     Q(user__email__icontains=keyword) | \
                     Q(mobile__icontains=keyword) | \
                     Q(student_id__icontains=keyword)

        return queryset \
            .annotate(full_name=Concat('user__first_name', Value(' '), 'user__last_name')) \
            .filter(or_filters)