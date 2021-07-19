from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.views.generic import DetailView, CreateView, View
from .models import Product, Smartphone, Notebook, Category, LatestProducts, Customer, Cart, CartProduct
from .mixins import CategoryDetailMixin


class BaseView(View):
    """Базовая страница"""

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        products = LatestProducts.objects.get_products_for_main_page('notebook', 'smartphone')
        context = {
            'categories': categories,
            'products': products
        }
        return render(request, "layout/base.html", context)


class ProductDetailView(CategoryDetailMixin, DetailView):
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
        return context


class CategoryDetailView(CategoryDetailMixin, DetailView):
    """Детальная информация по категориям"""
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'mainapp/category_detail.html'
    slug_url_kwarg = 'slug'


class AddToCartView(View):
    """Добавление товара в корзину"""

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        # Получаем текущего пользователя
        customer = Customer.objects.get(user=request.user)
        # Получаем корзину привязываемую к пользователяю, in_order - активная только одна
        cart = Cart.objects.get(owner=customer, in_order=False)
        # Определяем модель для товара
        content_type = ContentType.objects.get(model=ct_model)
        # Получаем продукт обращаясь через content_type к родительской модели.
        # Далее через менеджер(objects) получаем продук по product_slug
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.create(
            user=cart.owner, cart=cart, content_object=product, final_price=product.price
        )
        cart.products.add(cart_product)
        # Редирект в корзину, разделители в данном случае КРАЙНЕ важны для построение url адреса.
        return HttpResponseRedirect('/shop/cart/')


class CartView(View):
    """Рендеринг корзины"""

    def get(self, request, *args, **kwargs):
        # Берётся текущий пользователь
        customer = Customer.objects.get(user=request.user)
        cart = Cart.objects.get(owner=customer)
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': cart,
            'categories': categories
        }
        return render(request, 'mainapp/cart.html', context)
