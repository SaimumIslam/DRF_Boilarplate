import os
import binascii
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, ContentType, Permission, Group

from base import models as base_models

from .utils import role, timezone
from .core.managers import UserManager, TokenManager


class Institute(base_models.BaseModel):
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField()
    mobile = base_models.PhoneNumberField()
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Branch(base_models.BaseModel):
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE, related_name="branches")
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField()
    mobile = base_models.PhoneNumberField()
    address = models.TextField(null=True, blank=True)
    timezone = models.CharField(max_length=50, choices=timezone.TIMEZONE_CHOICES, default=settings.TIME_ZONE)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return "{} : {}".format(self.institute.name, self.name)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=5, choices=role.ROLE_CHOICES)
    is_staff = models.BooleanField(default=False, help_text="Admin site access.")
    is_active = models.BooleanField(default=True, help_text="Unselect instead of deleting")
    branch = models.ForeignKey(Branch, null=True, on_delete=models.SET_NULL)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=["email"]),
        ]

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def __str__(self):
        return f'{self.email} {self.get_full_name()}'


class Profile(base_models.BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    student_id = models.CharField(max_length=25, null=True, blank=True)
    mobile = base_models.PhoneNumberField()
    address = models.TextField(null=True, blank=True)
    photo = models.URLField(null=True, blank=True)
    timezone = models.CharField(max_length=50, choices=timezone.TIMEZONE_CHOICES, default=settings.TIME_ZONE)
    last_activity_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["student_id"]),
        ]

    def __str__(self):
        return f'{self.user.get_full_name()}'


class Token(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    device_info = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s")

    objects = TokenManager()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return f' {self.key} {self.user.email}'

# user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
# no_spaces_string = user_agent.replace(" ", "")
