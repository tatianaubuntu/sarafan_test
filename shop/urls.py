from django.urls import path
from shop.apps import ShopConfig
from shop.views import CategoryListAPIView, ProductListAPIView, CartProductCreateAPIView, CartProductUpdateAPIView, \
    CartProductDestroyAPIView, CartListAPIView, CartDestroyAPIView

app_name = ShopConfig.name

urlpatterns = [
    path('category/', CategoryListAPIView.as_view(), name='category-list'),
    path('product/', ProductListAPIView.as_view(), name='product-list'),
    path('cart_product/create/', CartProductCreateAPIView.as_view(), name='cart_product-create'),
    path('cart_product/update/<int:pk>/', CartProductUpdateAPIView.as_view(), name='cart_product-update'),
    path('cart_product/delete/<int:pk>/', CartProductDestroyAPIView.as_view(), name='cart_product-delete'),
    path('cart/', CartListAPIView.as_view(), name='cart-list'),
    path('cart/delete/', CartDestroyAPIView.as_view(), name='cart-delete'),
]
