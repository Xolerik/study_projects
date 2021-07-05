from django.forms import ModelChoiceField
from django.contrib import admin
from .models import *

class NotebookAdmin(admin.ModelAdmin):
    """Отображение категории в админке"""
    list_display = ("title", "price", "diagonal", "resolution")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Сравнение поля из БД
        if db_field.name == "category":
            # Используется класс-заглушка, который возвращает одно заранее отфильтрованное значение
            return ModelChoiceField(Category.objects.filter(slug="notebooks"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):
    """Отображение категории в админке"""
    list_display = ("title", "price", "diagonal", "resolution")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Сравнение поля из БД
        if db_field.name == "category":
            return ModelChoiceField(Category.objects.filter(slug="smartphones"))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartProduct)