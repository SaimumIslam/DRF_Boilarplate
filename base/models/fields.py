from django.db.models import CharField
from django.utils.translation import gettext_lazy as _

from ..core import validators


class PhoneNumberField(CharField):
    default_validators = [validators.phone_validator]
    description = _("Phone number")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("max_length", 16)
        min_length = kwargs.pop("min_length", 5)

        super().__init__(*args, **kwargs)

        if min_length is not None:
            self.validators.append(validators.MinLengthValidator(min_length))
