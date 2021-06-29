from django.forms import ModelForm
from .models import AMDVideo, AMDProcessor


class AMDVideoForm(ModelForm):
    class Meta:
        # Модель, для которой делается форма
        model = AMDVideo
        # Последовательность имён полей, которые должны присутствовать в форме
        fields = ["full_name", "abbreviated_name", "price", "amount", "name_chipset", "line_chipset", "vram",
                  "vram_type",
                  "directx", "video_partners", "content", "product_section_amd_videcard"]
