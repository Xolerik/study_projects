from decimal import Decimal
from django.conf import settings
from ..main_shop.models import AMDVideo


class Cart(object):
    def __init__(self, request):
        """Инициализация корзины"""
        # Текущая сессия
        self.session = request.session
        # Получение корзины из текущей сессии
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        """Хранение сессии"""
        # Обновление сессии
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметка сеанса как изменённого, чтобы убедиться, что он сохранился
        self.session.modified = True

    def add(self):
        """Добавление товара в корзину или обновление его количества"""
        product_id = str(AMDVideo.id)
        if product_id not in self.cart:
            self.cart