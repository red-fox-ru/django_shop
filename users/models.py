from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django_countries.fields import CountryField

class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_("first name"), max_length=128, blank=True)
    last_name = models.CharField(_("last name"), max_length=128, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    country = CountryField(blank_label='(select country)', multiple=False)
    phone = models.IntegerField(validators=[
            MaxValueValidator(9999999999),
            MinValueValidator(1000000000)
        ], blank=True, null=True)

    def __str__(self):
        return self.username
