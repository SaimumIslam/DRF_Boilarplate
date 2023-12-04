from django.db.models.signals import post_save
from django.dispatch import receiver

from .services.group import GroupService
from .services.user import UserService

from .models import User


def create_permission_groups(sender, **kwargs):
    # connect to signal in apps.py
    group_service = GroupService()
    group_service.post_migration_create()

    # new 'permission' table record should be added in 'group_permissions' table


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return
    user_service = UserService()
    user_service.post_save(instance)
