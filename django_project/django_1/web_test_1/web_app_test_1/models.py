from django.db import models
from django.core.validators import MinValueValidator, ValidationError


class Bd(models.Model):
    """Класс для описания объявления"""
    title = models.CharField(max_length=50, verbose_name='Наименование товара')
    content = models.TextField(null=True, blank=True, verbose_name='Описание товара')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена', help_text='Мин: 5000',
                              validators=[MinValueValidator(5000, ('Минимальная цена товара 5000'))])
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')
    # Внешний ключ. Привязка контента к рубрике.
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')

    def clean(self):
        """Валидация модели"""
        errors = {}
        if not self.content:
            errors['content'] = ValidationError("Укажите описание продаваемого товара")

        if not self.price:
            errors['price'] = ValidationError("Укажите стоимость товара")

        if not self.title:
            errors['title'] = ValidationError("Укажите наименование товара")

        if errors:
            raise ValidationError(errors)

    class Meta:
        """Параметры модели"""
        # Последовательность имён полей, которые должны хранить уникальные в пределах таблицы значения
        unique_together = ('title', 'published')
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        # Сортировка
        ordering = ['-published']

class Rubric(models.Model):
    """Класс для описания рубрики"""
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')

    def __str__(self):
        """Строковое представление"""
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']
