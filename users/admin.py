from django.contrib import admin
from django.utils.safestring import mark_safe

from users.models import User
from django import forms


class ImageAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['img'].help_text = mark_safe(
            "<span style='color:red;'> Изображение с разрешением больше 1080х1080 будет обрезано</span>"
        )


class UsersAdmin(admin.ModelAdmin):
    form = ImageAdminForm


admin.site.register(User, UsersAdmin)
