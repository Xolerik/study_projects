from django.views.generic.detail import SingleObjectMixin
from django.views.generic import View
from .models import Category, Cart, Customer, Notebook, Smartphone


class CategoryDetailMixin(SingleObjectMixin):
    """ Вывод в ниспадающее меню категории """

    CATEGORY_SLUG_TO_PRODUCT_MODEL = {
        'notebooks': Notebook,
        'smartphones': Smartphone,
    }

    def get_context_data(self, **kwargs):
        # Проверяем, относится ли object к Category
        if isinstance(self.get_object(), Category):
            # Обращаемся к инстансу категории. Получем модель через slug.
            model = self.CATEGORY_SLUG_TO_PRODUCT_MODEL[self.get_object().slug]
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.get_categories_for_left_sidebar()
            context['category_products'] = model.objects.all()
            return context
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.get_categories_for_left_sidebar()
        return context

class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Проверяем аутентификацию пользователя
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(user=request.user)
            # Возвращаем корзину конкретного пользователя (аутентифицированного)
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)