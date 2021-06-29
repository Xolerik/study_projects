import os
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models
from django.core.validators import ValidationError, MinValueValidator


class AMDVideo(models.Model):
    """Class for amd graphics cards"""

    class AMDChipset(models.TextChoices):
        RX550 = 'RX550', _('AMD Radeon™ RX 550')
        RX560 = 'RX560', _('AMD Radeon™ RX 560')
        RX570 = 'RX570', _('AMD Radeon™ RX 570')
        RX580 = 'RX580', _('AMD Radeon™ RX 580')
        RX590 = 'RX590', _('AMD Radeon™ RX 590')
        RX590GME = 'RX590GME', _('AMD Radeon™ RX 590 GME')

    class VideoRAM(models.TextChoices):
        GB_4 = '4.0GB', _('4.0 GB')
        GB_6 = '6.0GB', _('6.0 GB')
        GB_8 = '8.0GB', _('8.0 GB')
        GB_11 = '11.0GB', _('11.0 GB')

    class VideoRAMType(models.TextChoices):
        GDDR2 = '2', _('GDD2')
        GDDR3 = '3', _('GDDR3')
        GDDR4 = '4', _('GDDR4')
        GDDR5 = '5', _('GDDR5')
        GDDR5X = '5X', _('GDDR5X')
        GDDR6 = '6', _('GDDR6')
        GDDR6X = '6X', _('GDDR6X')

    class DirectX(models.TextChoices):
        directx9 = 'V9', _('DirectX Version 9')
        directx10 = 'V10', _('DirectX Version 10')
        directx11 = 'V11', _('DirectX Version 11')
        directx12 = 'V12', _('DirectX Version 12')

    class VideoPartners(models.TextChoices):
        asus = 'asus', _('ASUS')
        msi = 'msi', _('MSI')
        gigabyte = 'gig', _('Gigabyte')
        sapphire = 'sapphire', _('Sapphire')
        xfx = 'xfx', _('XFX')

    # def images_path(self):
    # Функция получения пути к картинке, требуется модуль pillow, позже следует разобраться
    #     return os.path.join(settings.LOCAL_FILE_DIR, "images")

    full_name = models.CharField(max_length=250, verbose_name="Полное наименование видеокарты", unique=True)
    abbreviated_name = models.CharField(max_length=65, verbose_name="Наименование товара",
                                        help_text="Сокращённое наименование для выводе в поиске")
    price = models.FloatField(verbose_name="Цена")
    amount = models.FloatField(blank=True, verbose_name="Количество единиц товара",
                               validators=[
                                   MinValueValidator(1, ("Минимально допустимое количество: 1 единица товара"))])
    name_chipset = models.ForeignKey('AMDVideoChipset', verbose_name='Чипсет', on_delete=models.PROTECT,
                                     default=1)
    line_chipset = models.ForeignKey('AMDLineVideoChipset', verbose_name="Линейка продуктов", on_delete=models.PROTECT,
                                     default=1)
    vram = models.CharField(verbose_name='Объем памяти', max_length=100, choices=VideoRAM.choices,
                            default=VideoRAM.GB_4)
    vram_type = models.CharField(verbose_name='Тип памяти', max_length=100, choices=VideoRAMType.choices,
                                 default=VideoRAMType.GDDR3)
    directx = models.CharField(verbose_name='Версия DirectX', max_length=25, choices=DirectX.choices,
                               default=DirectX.directx12)
    sli = models.BooleanField(verbose_name="Наличие SLI совместимости")
    video_partners = models.CharField(verbose_name="Производитель видеокарты", max_length=100,
                                      choices=VideoPartners.choices)
    date_added = models.DateTimeField(verbose_name='Дата добавления', auto_now_add=True, db_index=True)
    content = models.TextField(verbose_name="Описание товара", null=True, blank=True)
    product_section_amd_videcard = models.ForeignKey('ProductType', on_delete=models.PROTECT,
                                                     verbose_name="Выберите тип продукта: ")

    def clean(self):
        """Models field validator"""
        errors = {}
        if not self.price:
            errors['price'] = ValidationError("Требуется указать цену товара с НДС")
        if not self.vram:
            errors['vram'] = ValidationError("Требуется указать объем памяти")
        if not self.vram_type:
            errors['vram_type'] = ValidationError("Требуется указать тип памяти")
        if not self.abbreviated_name:
            errors['abbreviated_name'] = ValidationError("Требуется указать сокращённое наименование товара")
        if not self.directx:
            errors['directx'] = ValidationError("Требуется указать версию DirectX")
        if not self.video_partners:
            errors['video_partners'] = ValidationError("Требуется указать производителя видеокарты")
        if not self.line_chipset:
            errors['line_chipset'] = ValidationError("Требуется указать линейку чипсета")
        if not self.name_chipset:
            errors["name_chipset"] = ValidationError("Требуется указать наименование чипсета")
        if errors:
            raise ValidationError(errors)

    class Meta:
        """Model params"""
        unique_together = ("full_name", "abbreviated_name")
        ordering = ["video_partners"]
        verbose_name_plural = "Видеокарты AMD"
        verbose_name = "Видеокарта AMD"


class AMDVideoChipset(models.Model):
    name_chipset = models.CharField(verbose_name="Наименование чипсета", max_length=100)

    def __str__(self):
        return self.name_chipset

    def clean(self):
        errors = {}
        if not self.name_chipset:
            errors["name_chipset"] = ValidationError("Требуется заполнить поле")
        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name = "Чипсет видеокарты"
        verbose_name_plural = "Чипсеты видеокарт"
        ordering = ['name_chipset']


class AMDLineVideoChipset(models.Model):
    line_chipset = models.CharField(verbose_name="Линейка продуктов", max_length=100)

    def __str__(self):
        return self.line_chipset

    def clean(self):
        errors = {}
        if not self.line_chipset:
            errors['line_chipset'] = ValidationError("Требуется заполнить поле")
        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name = "Линейка чипсетов видеокарт"
        verbose_name_plural = "Линейки чипсетов видеокарт"
        ordering = ['line_chipset']


class AMDProcessor(models.Model):
    """Class for AMD processors"""

    class AMDProcessorSeries(models.TextChoices):
        SERIES1000 = "1000", _("AMD Ryzen™ 1000")
        SERIES1000Radeon = "1000Radeon", _("AMD Ryzen™ 1000 with Radeon Graphic")
        SERIES2000 = "2000", _("AMD Ryzen™ 2000")
        SERIES2000Radeon = "2000Radeon", _("AMD Ryzen™ 2000 with Radeon Graphic")
        SERIES3000 = "3000", _("AMD Ryzen™ 3000")
        SERIES3000Radeon = "3000Radeon", _("AMD Ryzen™ 3000 with Radeon Graphic")
        SERIES5000 = "5000", _("AMD Ryzen™ 5000")
        SERIES5000Radeon = "5000Radeon", _("AMD Ryzen™ 5000 with Radeon Graphic")

    full_name = models.CharField(verbose_name='Полное наименование процессора', max_length=150, unique=True)
    abbreviated_name = models.CharField(verbose_name='Наименование процессора', max_length=65,
                                        help_text="Сокращённое наименование процессора для отображения")
    content = models.TextField(verbose_name="Описание товара", null=True, blank=True)
    price = models.FloatField(verbose_name="Цена")
    amount = models.FloatField(blank=True, verbose_name="Количество единиц товара",
                               validators=[
                                   MinValueValidator(1, ("Минимально допустимое количество: 1 единица товара"))])
    processor_chipset = models.ForeignKey("AMDProcessorChipsetName", verbose_name="Чипсет процессора",
                                          on_delete=models.PROTECT)
    processor_socket = models.ForeignKey("AMDProcessorSocket", verbose_name="Тип сокета процессора",
                                         on_delete=models.PROTECT)
    cores = models.PositiveSmallIntegerField(verbose_name="Количество ядер в процессоре",
                                             validators=[MinValueValidator(1, ("Минимально допустимое значение: 1"))])
    series = models.CharField(verbose_name="Серия", max_length=50, choices=AMDProcessorSeries.choices,
                              default=AMDProcessorSeries.SERIES1000)
    date_added = models.DateField(verbose_name="Дата добавления", db_index=True, auto_now_add=True)
    product_setion_amd_processor = models.ForeignKey('ProductType', on_delete=models.PROTECT,
                                                     verbose_name="Выберите тип устройства: ")


class AMDProcessorSocket(models.Model):
    """Class for Models line"""
    socket_name = models.CharField(verbose_name="Тип сокета процесора", max_length=100)

    def __str__(self):
        return self.socket_name

    def clean(self):
        errors = {}
        if not self.socket_name:
            errors["socket_name"] = ValidationError("Требуется указать тип сокета")
        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name = ("Сокет")
        verbose_name_plural = ("Сокеты")


class AMDProcessorChipsetName(models.Model):
    name_chipset = models.CharField(verbose_name="Наименование чипсета процессора", max_length=100)

    def __str__(self):
        return self.name_chipset

    def clean(self):
        errors = {}
        if not self.name_chipset:
            errors["name_chipset"] = ValidationError("Требуется указать наименование чипсета")
        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name = ("Наименование чипсета процессора")
        verbose_name_plural = ("Наименования чипсетов процессоров")


class ProductType(models.Model):
    """Section products"""
    full_name = models.CharField(max_length=250, db_index=True, verbose_name="Тип устройства")

    def __str__(self):
        return self.full_name

    class Meta:
        unique_together = ('full_name',)
        verbose_name_plural = "Устройство"
        verbose_name = "Устройства"
