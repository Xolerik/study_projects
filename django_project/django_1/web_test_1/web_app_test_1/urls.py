from django.urls import path
from .views import index, by_rubric, BdCreateView
"""Файл для создания маршрутов уровня приложения"""


urlpatterns = [
    # Угловые скобки обозначают описание URL параметра
    # rubric_id - имя параметра контроллера, которому будет присвоено значение этого URL-параметра
    path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('', index, name='index'),
    # Когда указывается контроллер-класс, требуется результат, что возвращается методом as_view()
    path('add/', BdCreateView.as_view(), name='add')
]
