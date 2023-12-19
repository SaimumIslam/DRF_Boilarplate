from django.db import models
from .fields import PhoneNumberField


# Create your models here.
class Model(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey('authentication.User', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="created_%(app_label)s_%(class)s")
    updated_by = models.ForeignKey('authentication.User', null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="updated_%(app_label)s_%(class)s")

    class Meta:
        abstract = True
