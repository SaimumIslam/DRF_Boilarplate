from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.regex_helper import _lazy_re_compile
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator

@deconstructible
class PhoneNumberValidator:
    message = _("Enter a valid phone.")
    code = "invalid"
    number_regx = _lazy_re_compile(r"^\+\d+$")

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):

        if not self.number_regx.match(value):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def __eq__(self, other):
        return (
                isinstance(other, PhoneNumberValidator)
                and (self.message == other.message)
                and (self.code == other.code)
        )


phone_validator = PhoneNumberValidator()
