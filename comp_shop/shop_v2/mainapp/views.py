from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView, CreateView, View
from .models import Product, Smartphone, Notebook, Category, LatestProducts, Customer, Cart, CartProduct
from .mixins import CategoryDetailMixin, CartMixin
from .forms import OrderForm, RegisterUserForm
from django.contrib import messages
from .utils import recalc_cart
from django.db import transaction
from django.contrib.auth.models import User
# Стандартная форма регистрации пользователя
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy



class BaseView(CartMixin, View):
    """Базовая страница"""

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        products = LatestProducts.objects.get_products_for_main_page('notebook', 'smartphone')
        context = {
            'categories': categories,
            'products': products,
            'cart': self.cart,
        }
        return render(request, "layout/base.html", context)


class ChangeQTYView(CartMixin, View):
    """Изменение количества товара в корзине"""

    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        # Определяем модель для товара
        content_type = ContentType.objects.get(model=ct_model)
        # Получаем продукт обращаясь через content_type к родительской модели.
        # Далее через менеджер(objects) получаем продук по product_slug
        product = content_type.model_class().objects.get(slug=product_slug)
        # Получаем корзину с указанными параметрами
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id,
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Количество изменено")
        return HttpResponseRedirect('/shop/cart/')


class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):
    """Детальная информация о продукте"""

    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'mainapp/product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        """Получение контекста модели"""
        context = super().get_context_data(**kwargs)
        # Получение имени модели из скрытого метода _meta
        context['ct_model'] = self.model._meta.model_name
        # Добавление корзины в шаблон
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):
    """Детальная информация по категориям"""
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'mainapp/category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        """Получение контекста модели"""
        context = super().get_context_data(**kwargs)
        # Добавление корзины в шаблон
        context['cart'] = self.cart
        return context


class AddToCartView(CartMixin, View):
    """Добавление товара в корзин"""
    user = User
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
            # Определяем модель для товара
            content_type = ContentType.objects.get(model=ct_model)
            # Получаем продукт обращаясь через content_type к родительской модели.
            # Далее через менеджер(objects) получаем продук по product_slug
            product = content_type.model_class().objects.get(slug=product_slug)
            # На основании полученных данных создаём корзину для текущего покупателя
            # get_or_create возвращает кортеж из двух значений, где первое  - сам объект(полученный или созданный),
            # второе - булевое значение (был создан или нет).
            cart_product, created = CartProduct.objects.get_or_create(
                user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id,
            )
            if created:
                self.cart.products.add(cart_product)
            recalc_cart(self.cart)
            messages.add_message(request, messages.INFO, "Товар успешно добавлен")
            # Редирект в корзину, разделители в данном случае КРАЙНЕ важны для построение url адреса.
            return HttpResponseRedirect('/shop/cart/')
        else:
            # Редирект на страницу входа или создания аккаунта, разделители в данном случае КРАЙНЕ важны для построение url адреса.
            messages.add_message(request, messages.INFO, "Вход успешно выполнен.")
            return HttpResponseRedirect('/accounts/login/')

class DeleteFromCartView(CartMixin, View):
    """Удаление товара из корзины"""

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        # Определяем модель для товара
        content_type = ContentType.objects.get(model=ct_model)
        # Получаем продукт обращаясь через content_type к родительской модели.
        # Далее через менеджер(objects) получаем продук по product_slug
        product = content_type.model_class().objects.get(slug=product_slug)
        # Получаем корзину с указанными параметрами
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id,
        )
        self.cart.products.remove(cart_product)
        # Удаление корзины с продуктами
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно удалён")
        # Редирект в корзину, разделители в данном случае КРАЙНЕ важны для построение url адреса.
        return HttpResponseRedirect('/shop/cart/')


class CartView(CartMixin, View):
    """Рендеринг корзины"""

    def get(self, request, *args, **kwargs):
        # Берётся текущий пользователь
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'mainapp/cart.html', context)


class CheckOutViews(CartMixin, View):
    """Рендеринг формы заказа"""

    def get(self, request, *args, **kwargs):
        # Берётся текущий пользователь
        categories = Category.objects.get_categories_for_left_sidebar()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'mainapp/checkout.html', context)


class MakeOrderView(CartMixin, View):
    """Создание заказа"""

    # В случае того, если что-то пойдёт не так - изменения откатятся.
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Спасибо за заказ! Менеджер с Вами свяжется')
            return HttpResponseRedirect('/shop')
        return HttpResponseRedirect('/checkout/')

class RegisterUser(CartMixin, CreateView):
    """Регистрация пользователя"""
    form_class = RegisterUserForm
    template_name = 'account/register.html'
    # Перенаправляет на адрес при успешной регистрации пользователя
    success_url = reverse_lazy('login')