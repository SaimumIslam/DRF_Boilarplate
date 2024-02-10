from django.db import models
from django.contrib import auth
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _


class GroupRestriction(models.Model):
    restriction = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="group_restrictions")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="group_restrictions")

    class Meta:
        db_table = "auth_group_restrictions"


class RestrictionsMixin(models.Model):
    user_restrictions = models.ManyToManyField(
        Permission,
        verbose_name=_("user restrictions"),
        blank=True,
        help_text=_("Specific restrictions for this user."),
        related_name="r_users",
        related_query_name="r_user",
    )

    class Meta:
        abstract = True

    def get_user_restrictions(self, obj=None):
        """
        Return a list of restrictions strings that this user has directly.
        Query all available auth backends. If an object is passed in,
        return only restrictions matching this object.
        """
        return _user_get_restrictions(self, obj, "user")

    def get_group_restrictions(self, obj=None):
        """
        Return a list of restrictions strings that this user has through their
        groups. Query all available auth backends. If an object is passed in,
        return only restrictions matching this object.
        """
        return _user_get_restrictions(self, obj, "group")

    def get_all_restrictions(self, obj=None):
        return _user_get_restrictions(self, obj, "all")


def _user_get_restrictions(user, obj, from_name):
    restrictions = set()
    name = "get_%s_restrictions" % from_name
    for backend in auth.get_backends():
        if hasattr(backend, name):
            restrictions.update(getattr(backend, name)(user, obj))
    return restrictions
