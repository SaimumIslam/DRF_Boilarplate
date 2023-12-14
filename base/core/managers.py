from django.db import models

from .querysets import QuerySet


class Manager(models.Manager):
    def get_queryset(self):
        return QuerySet(self.model, using=self._db)

    # def get_queryset(self):
    #     return super().get_queryset().filter(is_active=True)

    # def get_queryset(self):
    #     return super(Manager, self).get_queryset().filter(is_active=False)
