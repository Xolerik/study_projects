from django.shortcuts import render
from .models import AMDVideo, AMDVideoChipset, AMDLineVideoChipset, AMDProcessor, AMDProcessorSocket, \
    AMDProcessorChipsetName, ProductType
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import AMDVideoForm

class AMDVideoView(CreateView):
    """Контроллер-класс для вывода и обработки формы"""
    # The path to the template file that will be used to display the form
    template_name = 'main_shop/create.html'
    # The form to be used
    form_class = AMDVideoForm
    # Internet address to be used for forwarding after successful form creation
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        """Функция для формирования контекста шаблона"""
        context = super().get_context_data(**kwargs)
        context['ProductType']


def index(request):
    """Функция контроллер для стартовой страницы"""
    amdvideos = AMDVideo.objects.all()
    producttypes = ProductType.objects.all()
    # Контекст шаблона, ключ - имя переменной по которой доступны данные в самом шаблоне,
    # значение - сами данные получамые из БД
    context = {"amdvideos": amdvideos, "products": producttypes}
    return render(request, "main_shop/index.html", context)

def by_product(request, product_id):
    """Функция контроллер для рубрики"""
    # Фильтрация данных по внешнему id продукта
    producttypes = ProductType.objects.filter(product=product_id)