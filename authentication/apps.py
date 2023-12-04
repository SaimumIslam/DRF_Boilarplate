from django.apps import AppConfig
from django.db.models.signals import post_migrate


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

    def ready(self):
        from .signals import create_permission_groups
        post_migrate.connect(create_permission_groups, sender=self, dispatch_uid="create_permission_groups")
