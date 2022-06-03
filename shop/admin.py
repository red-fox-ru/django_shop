from django.contrib import admin
from django import forms

from shop.models import Category, RamProduct, NotebookProduct, SmartphoneProduct, CartProduct, Cart


class NotebookCategoryChoiceField(forms.ModelChoiceField):
    pass


class NotebookAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return forms.ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(NotebookProduct, NotebookAdmin)


class SmartphoneCategoryChoiceField(forms.ModelChoiceField):
    pass


class SmartphoneAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return forms.ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(SmartphoneProduct, SmartphoneAdmin)

admin.site.register(Category)
admin.site.register(RamProduct)
admin.site.register(CartProduct)
admin.site.register(Cart)
