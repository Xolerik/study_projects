from django.shortcuts import render
from .models import AMDVideo, AMDVideoChipset, AMDLineVideoChipset, AMDProcessor, AMDProcessorSocket, \
    AMDProcessorChipsetName, ProductType
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import AMDVideoForm


class AMDVideoView(CreateView):
    """Контроллер-класс для вывода и обработки формы модели AMDVideo"""
    # The path to the template file that will be used to display the form
    template_name = 'main_shop/create.html'
    # The form to be used
    form_class = AMDVideoForm
    # Internet address to be used for forwarding after successful form creation
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        """Функция для формирования контекста шаблона"""
        context = super().get_context_data(**kwargs)
        context['producttypes'] = AMDVideoChipset.objects.all()
        return context


def index(request):
    """Функция контроллер для стартовой страницы"""
    amdvideos = AMDVideo.objects.all()
    video_chiposet = AMDLineVideoChipset.objects.all()
    producttypes = ProductType.objects.all()
    # Контекст шаблона, ключ - имя переменной по которой доступны данные в самом шаблоне,
    # значение - сами данные получамые из БД
    context = {"amdvideos": amdvideos, "products": producttypes, "video_chiposet": video_chiposet}
    return render(request, "main_shop/index.html", context)


def video_chipset(request, video_chipset_id):
    """Функция контроллер для отображения чипсетов видеокарты"""
    video_chipset = AMDLineVideoChipset.objects.filter(video_chipset=video_chipset_id)
    current_video_chipset = AMDLineVideoChipset.objects.get(pk=video_chipset_id)
    context = {"video_chipset": video_chipset}
    return render(request, 'main_shop/video_chipset.html', context)

def video_cards(request):
    """Функция контроллер для отображения списка видеокарт"""
    video_chiposet = AMDLineVideoChipset.objects.all()
    context = {"video_chiposet": video_chiposet}
    return render(request, "main_shop/video_cards.html", context)

def product_type(request, product_id):
    """Функция контроллер для типо продукта"""
    # Фильтрация данных по внешнему id продукта
    producttypes = ProductType.objects.filter(product=product_id)
    # Выбор всех типов продуктов
    current_producttype = ProductType.objects.get(pk=product_id)
    context = {"producttypes": producttypes, "current_producttype": current_producttype}
    return render(request, 'main_shop/product_types.html', context)
