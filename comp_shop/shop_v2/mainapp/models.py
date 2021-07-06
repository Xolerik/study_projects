from django.db import models
from django.contrib.auth import get_user_model
# ContentType - мини фреймворк, который видит все модели из приложений, которые есть в Installed_apps в settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

# Параметры берутся из settings.AUTH_USER_MODEL (само поле скрыто, но есть значения по умолчанию)
User = get_user_model()


class LatestProductsManager:
    """Очень сомнительный класс, следует переписать код в файле view применяя пагинатор"""

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get("with_respect_to")
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__.meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:
    objects = LatestProductsManager


class Category(models.Model):
    """Наименование категории"""
    name = models.CharField(max_length=255, verbose_name="Наименование категории")
    slug = models.SlugField(unique=True)

    def __str__(self):
        """Возвращает строкове представление для админки сайта"""
        return self.name


class Product(models.Model):
    """Продукт"""
    category = models.ForeignKey("Category", verbose_name="Категория", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Наименование")
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name="Изображение",
                              help_text="Загружайте изображение разрешением минимум 400х400")
    description = models.TextField(verbose_name="Описание товара", null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Цена")

    def __str__(self):
        return self.title

    def clean(self):
        """Проверка размера изображения"""
        if not self.image:
            raise ValidationError("Требуется загрузить изображение")
        else:
            w, h = get_image_dimensions(self.image)
            if w <= 400:
                raise ValidationError(f"Требуемое разрешения для загрузки от 400. У текущего изображения{w} ")
            if h <= 400:
                raise ValidationError(f"Требуемое разрешения для загрузки от 400. У текущего изображения{h} ")

    class Meta:
        abstract = True


class Notebook(Product):
    """Ноутбуки"""
    diagonal = models.CharField(max_length=50, verbose_name="Диагональ")
    display_type = models.CharField(max_length=50, verbose_name="Тип дисплэя")
    resolution = models.CharField(max_length=100, verbose_name="Разрешение экрана")
    processor_freq = models.CharField(max_length=50, verbose_name="Частота процессора")
    ram = models.CharField(max_length=100, verbose_name="Оперативная память")
    video = models.CharField(max_length=100, verbose_name="Видеокарта")
    time_without_charge = models.CharField(max_length=5, verbose_name="Время работы от аккумулятора")

    def __str__(self):
        return f"{self.category.name} : {self.title}"


class Smartphone(Product):
    """Смартфоны"""
    diagonal = models.CharField(max_length=50, verbose_name="Диагональ")
    display_type = models.CharField(max_length=50, verbose_name="Тип дисплэя")
    resolution = models.CharField(max_length=100, verbose_name="Разрешение экрана")
    accum_value = models.CharField(max_length=100, verbose_name="Объем аккумулятора")
    ram = models.CharField(max_length=100, verbose_name="Оперативная память")
    # Возможность добавлять внешнюю память
    sd = models.BooleanField(default=True)
    sd_value_max = models.CharField(max_length=100, verbose_name="Максимальный объем встраиваемой памяти")
    main_cam_mp = models.CharField(max_length=20, verbose_name="Главная камера")
    frontal_cam_mp = models.CharField(max_length=20, verbose_name="Фронтальная камера")

    def __str__(self):
        return f"{self.category.name} : {self.title}"


class CartProduct(models.Model):
    """Заглушка - продукт корзины"""
    user = models.ForeignKey("Customer", verbose_name="Покупатель", on_delete=models.CASCADE)
    cart = models.ForeignKey("Cart", verbose_name="Корзина", on_delete=models.CASCADE, related_name="related_products")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    # Количество
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая стоимость")

    def __str__(self):
        return f"Продукт: {self.product.title}"


class Cart(models.Model):
    """Корзина"""
    owner = models.ForeignKey("Customer", verbose_name="Владелец", on_delete=models.CASCADE)
    products = models.ManyToManyField("CartProduct", blank=True, related_name="related_cart")
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Общая стоимость")

    def __str__(self):
        return f"Корзина: {self.owner}"


class Customer(models.Model):
    """Покупатель"""
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=255, verbose_name="Адрес")

    def __str__(self):
        return f"Покупатель: {self.user.first_name} {self.user.last_name}"
