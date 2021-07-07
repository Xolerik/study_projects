from django.shortcuts import render
from django.views.generic import DetailView
from .models import Product, Smartphone
# Create your views here.
def index(request):
    # """Функция контроллер для стартовой страницы"""
    # amdvideos = AMDVideo.objects.all()
    # video_chipset = AMDLineVideoChipset.objects.all()
    # producttypes = ProductType.objects.all()
    # # Контекст шаблона, ключ - имя переменной по которой доступны данные в самом шаблоне,
    # # значение - сами данные получамые из БД
    # context = {
    #     "amdvideos": amdvideos,
    #     "products": producttypes,
    #     "video_chipset": video_chipset
    # }
    # return render(request, "main_shop/index.html", context)
    return render(request, "mainapp/base.html", {})

class ProductDetailView(DetailView):
    model = Smartphone
    context_object_name = "smartphones"
    template_name = "mainapp/product_detail.html"
    slug_url_kwarg = "slug"