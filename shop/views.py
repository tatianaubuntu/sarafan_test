from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shop.models import Category, Product, CartProduct
from shop.paginators import PageNumPagination
from shop.serializers import CategorySerializer, ProductSerializer, \
    CartProductSerializer, CartProductUpdateSerializer, CartSerializer
from users.models import User
from users.permissions import IsUser


class CategoryListAPIView(generics.ListAPIView):
    """Контроллер вывода списка категорий, подкатегорий постранично"""
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(level=0)
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumPagination


class ProductListAPIView(generics.ListAPIView):
    """Контроллер вывода списка продуктов постранично"""
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumPagination


class CartProductCreateAPIView(generics.CreateAPIView):
    """Контроллер добавления продукта в корзину"""
    serializer_class = CartProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Добавляет продукт в корзину"""
        new_product = serializer.save()
        new_product.price = new_product.product.price
        new_product.total_price = new_product.price * new_product.quantity
        new_product.save()


class CartProductUpdateAPIView(generics.UpdateAPIView):
    """Контроллер изменения количества продукта в корзине"""
    serializer_class = CartProductUpdateSerializer
    queryset = CartProduct.objects.all()
    permission_classes = [IsAuthenticated, IsUser]

    def perform_update(self, serializer):
        """Изменяет количество продукта в корзине"""
        product = serializer.save()
        product.price = product.product.price
        product.total_price = product.price * product.quantity
        product.save()


class CartProductDestroyAPIView(generics.DestroyAPIView):
    """Контроллер удаления продукта из корзины"""
    queryset = CartProduct.objects.all()
    permission_classes = [IsAuthenticated, IsUser]


class CartListAPIView(generics.ListAPIView):
    """Контроллер вывода списка продуктов в корзине"""
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsUser]

    def get_queryset(self):
        """Возвращает Queryset продуктов текущего пользователя"""
        queryset = User.objects.filter(id=self.request.user.pk)
        return queryset


class CartDestroyAPIView(generics.DestroyAPIView):
    """Контроллер удаления всех продуктов из корзины"""
    permission_classes = [IsAuthenticated, IsUser]

    def get_queryset(self):
        """Возвращает Queryset продуктов для удаления из корзины"""
        queryset = CartProduct.objects.filter(user=self.request.user)
        return queryset

    def delete(self, request, *args, **kwargs):
        """Удаляет все продукты из корзины"""
        instance = self.get_queryset()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
