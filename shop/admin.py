from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from shop.models import Category, RamProduct, NotebookProduct, SmartphoneProduct, CartProduct, Cart, Product


class ImageAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            "Изображение с минимальным разрешением {}х{}".format(*Product.MIN_RESOLUTION)
        )


class NotebookAdmin(admin.ModelAdmin):
    form = ImageAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return forms.ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(NotebookProduct, NotebookAdmin)


class SmartphoneAdmin(admin.ModelAdmin):
    form = ImageAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return forms.ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(SmartphoneProduct, SmartphoneAdmin)
admin.site.register(Category)
admin.site.register(RamProduct)
admin.site.register(CartProduct)
admin.site.register(Cart)
