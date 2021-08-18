from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Order


class OrderForm(forms.ModelForm):
    """Форма заказа"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.fields['order_date'].label = 'Дата получения заказа'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order

        fields = (
            'first_name', 'last_name', 'phone', 'address', 'buying_type', 'order_date', 'comment',
        )

class RegisterUserForm(UserCreationForm):
    """Форма регистрации пользователя"""
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }