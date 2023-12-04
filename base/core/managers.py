from django.db import models

from .querysets import BaseQuerySet


class BaseManager(models.Manager):
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db)

    # def get_queryset(self):
    #     return super().get_queryset().filter(is_active=True)

    # def get_queryset(self):
    #     return super(BaseManager, self).get_queryset().filter(is_active=False)
