from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class PhoneValidator(validators.RegexValidator):
    regex = r"^"
    message = _(
        "Enter a valid username. This value may contain only letters, "
        "numbers, and @/./+/-/_ characters."
    )
    flags = 0

class User(AbstractUser):
    phone_validator = PhoneValidator()

    phone_number = models.CharField(
        max_length = 13,
        verbose_name = "Phone number",
        validators = [phone_validator],
        unique=True,
        error_messages = {
            "unique": "Bunday telefon raqam allaqachon mavjud!"
        }
    )

