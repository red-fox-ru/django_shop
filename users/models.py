import sys
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django_countries.fields import CountryField
from PIL import Image
from io import BytesIO


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
    img = models.ImageField(upload_to='users_image', blank=True, verbose_name="Аватар")
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

    def save(self, *args, **kwargs):
        if self.img:
            avatar = Image.open(self.img)
            if avatar.width > 1080 or avatar.height > 1080:
                new_img = avatar.convert('RGB')
                resized_img = new_img.resize((1080, 1080), Image.ANTIALIAS)
                file_ = BytesIO()
                resized_img.save(file_, 'JPEG', quality=90)
                file_.seek(0)
                name = '{}.{}'.format(*self.img.name.split('.'))
                self.image = InMemoryUploadedFile(file_, 'ImageField', name, 'jpeg/image', sys.getsizeof(file_), None)
                super().save(*args, **kwargs)
        super().save(*args, **kwargs)
