from django.urls import path
from .views import (
    ProductDetailView,
    CategoryDetailView,
    BaseView,
    CartView,
    AddToCartView,
    DeleteFromCartView,
    ChangeQTYView,
    CheckOutViews,
    MakeOrderView,
    RegisterUser,
)

urlpatterns = [
    path('', BaseView.as_view(), name="base"),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name="product_detail"),
    path('category/<str:slug>', CategoryDetailView.as_view(), name="category_detail"),
    path('cart/', CartView.as_view(), name="cart"),
    path('add_to_cart/<str:ct_model>/<str:slug>', AddToCartView.as_view(), name="add_to_cart"),
    path('remove_from_cart/<str:ct_model>/<str:slug>', DeleteFromCartView.as_view(), name="delete_from_cart"),
    path('change_qty/<str:ct_model>/<str:slug>', ChangeQTYView.as_view(), name="change_qty"),
    path('checkout/', CheckOutViews.as_view(), name="checkout"),
    path('make_order/', MakeOrderView.as_view(), name="make_order"),
    path('register/', RegisterUser.as_view(), name="register"),
]
