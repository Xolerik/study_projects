from django.contrib import admin
from .models import AMDVideo, AMDVideoChipset, AMDLineVideoChipset, AMDProcessor, AMDProcessorSocket, \
    AMDProcessorChipsetName, ProductType


# Register your models here.
class AMDVideoAdmin(admin.ModelAdmin):
    """Класс редактор модели AMDVideo в админке"""
    # Последовательность имён полей, которые должны выводиться в списке записей
    list_display = ("product_section_amd_videcard", "abbreviated_name", "price", "video_partners", "vram")


class AMDVideoChipsetAdmin(admin.ModelAdmin):
    """Класс редактор модели AMDVideoChipset в админке"""
    # Последовательность имён полей, которые должны выводиться в списке записей
    list_display = ("name_chipset",)


class AMDLineVideoChipsetAdmin(admin.ModelAdmin):
    list_display = ("line_chipset",)


class AMDProcessorAdmin(admin.ModelAdmin):
    list_display = (
    "product_setion_amd_processor", "abbreviated_name", "price", "processor_chipset", "processor_socket", "cores",
    "amount")


# Регистрация модели БД в админке:
# 1 параметр - сама модель БД,
# 2 параметр - класс редактор для представления данных из модели в админке
admin.site.register(AMDVideo, AMDVideoAdmin)
admin.site.register(AMDVideoChipset, AMDVideoChipsetAdmin)
admin.site.register(AMDLineVideoChipset, AMDLineVideoChipsetAdmin)
admin.site.register(AMDProcessor, AMDProcessorAdmin)
admin.site.register(ProductType)
