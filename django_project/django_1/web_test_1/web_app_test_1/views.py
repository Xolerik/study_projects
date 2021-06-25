from django.shortcuts import render
# Базовый класс реализует функциональность по созданию
# формы, выводу ее на экран с применением указанного шаблона, получению
# занесенных в форму данных, проверке их на корректность, сохранению их в новой
# записи модели и перенаправлению в случае успеха на интернет-адрес, который мы
# зададим.
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Bd, Rubric
from .forms import BdForm

class BdCreateView(CreateView):
    """Контроллер-класс для вывода и обработки формы"""
    # The path to the template file that will be used to display the form
    template_name = 'web_app_test_1/create.html'
    # The form to be used
    form_class = BdForm
    # Internet address to be used for forwarding after successful form creation
    # Функция reverse_lazy() принимает в качестве параметров имя маршрута и его параметры
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        """Функция для формирования контекста шаблона"""
        # Делегирует вызов метода классу-родителю(или классу-собрату)
        context = super().get_context_data(**kwargs)
        # Добавляем список рубрик в метод базового класса
        context['rubrics'] = Rubric.objects.all()
        return context

def index(request):
    """Функция контроллер для стартовой страницы"""
    # Реализован вывод панели навигации
    # Загрузка шаблона из указанной папки (по умолчанию шаблонизатор ищет шаблоны в папке templates в корне приложения)
    # Поменялось использование, т.к. был записан метод render и получение шаблона происходит в нём
    # template = loader.get_template('web_app_test_1/index.html')
    # Получение данных из БД
    bbs = Bd.objects.all()
    rubrics = Rubric.objects.all()
    # Контекст шаблона, ключ - имя переменной по которой доступны данные в самом шаблоне,
    # значение - сами данные получамые из БД
    context = {'bbs': bbs, 'rubrics': rubrics}
    return render(request, 'web_app_test_1/index.html', context)

def by_rubric(request, rubric_id):
    """Функция конт-роллер для рубрик"""
    # Фильтрация данных по внешнему id рубрики
    bbs = Bd.objects.filter(rubric=rubric_id)
    # Список всех рубрик
    rubrics = Rubric.objects.all()
    # Текущая рубрика
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'web_app_test_1/by_rubric.html', context)