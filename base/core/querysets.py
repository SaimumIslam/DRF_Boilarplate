from django.db import models


class QuerySet(models.QuerySet):
    def alive(self):
        return self.filter(is_active=True)

    def dead(self):
        return self.exclude(is_active=True)
