from django.shortcuts import render

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