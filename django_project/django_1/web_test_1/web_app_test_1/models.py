from django.db import models


class Bd(models.Model):
    """Класс для описание объявления"""
    title = models.CharField(max_length=50, verbose_name='Наименование товара')
    content = models.TextField(null=True, blank=True, verbose_name='Описание товара')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации0')
    # Внешний ключ. Привязка контента к рубрике.
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')

    class Meta:
        """Класс для объявления текстовых представлений"""
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published']


class Rubric(models.Model):
    """Класс для описания рубрики"""
    # Наименование рубрики
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')

    def __str__(self):
        """Функция создания строкового представления в админке"""
        # В данном случае возвращает наименование категории
        return self.name

    class Meta:
        """Класс для объявления текстовых представлений"""
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']
