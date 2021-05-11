from django.forms import ModelForm
from .models import Bd


class BdForm(ModelForm):
    class Meta:
        # Модель, для которой делается форма
        model = Bd
        # Последовательность имён полей, которые должны присутствовать в форме
        fields =['title', 'content', 'price', 'rubric']