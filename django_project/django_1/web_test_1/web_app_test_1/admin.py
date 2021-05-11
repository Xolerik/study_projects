from django.contrib import admin
from .models import Bd, Rubric


# Register your models here.

class BdAdmin(admin.ModelAdmin):
    """Класс редактор модели Bd в админке"""
    # Последовательность имён полей, которые должны выводиться в списке записей
    list_display = ('title', 'content', 'price', 'published', 'rubric')
    # Последовательность имён полей, которые преобразуются в гиперссылки
    list_display_links = ('title', 'content')
    # Последовательность имён полей, по которым выполняется фильтрация
    search_fields = ('title', 'content')


# Регистрация модели БД в админке:
# 1 параметр - сама модель БД,
# 2 параметр - класс редактор для представления данных из модели в админке
admin.site.register(Rubric)
admin.site.register(Bd, BdAdmin)
