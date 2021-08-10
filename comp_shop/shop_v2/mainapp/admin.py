from django.forms import ModelChoiceField, ModelForm
from django.contrib import admin
from .models import *


class SmartphoneAdminForm(ModelForm):
    """Отрисовка флажка SD карты при рендеринге формы"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Обращение к экземпляру формы
        instance = kwargs.get('instance')
        # Проверка чекбокса sd и переопределение атрибутов виджета для поля sd_volume_max
        if instance and not instance.sd:
            self.fields['sd_volume_max'].widget.attrs.update({
                'readonly': True, 'style ': 'background: lightgrey'
            })

    def clean(self):
        """Метод для работы с полями формы"""
        # Условия для пустого чекбокса sd карты
        if not self.cleaned_data['sd']:
            self.cleaned_data['sd_volume_max'] = None
        return self.cleaned_data


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
    # Шаблон для изменения стандартного шаблона админки
    change_form_template = 'mainapp/admin.html'
    # Присоединяем кастомную форму к стандартной
    form = SmartphoneAdminForm

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
admin.site.register(Order)