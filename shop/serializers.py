from django.db.models import Sum
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from shop.models import Category, Product, CartProduct
from shop.validators import QuantityValidator, ProductValidator
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории, подкатегории"""
    subcategory = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['title', 'image', 'slug', 'subcategory']

    @staticmethod
    def get_subcategory(obj):
        """Метод возвращает подкатегории соответствующей категории"""
        return CategorySerializer(obj.get_children(), many=True).data


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор продукта"""
    images = SerializerMethodField()

    class Meta:
        model = Product
        fields = ['title', 'slug', 'category', 'subcategory', 'price', 'images']

    @staticmethod
    def get_images(obj):
        """Метод возвращает список изображений"""
        if obj.image_1 and obj.image_2:
            image = obj.image.url
            image_1 = obj.image_1.url
            image_2 = obj.image_2.url
            images = [image, image_1, image_2]
            return images
        return None


class CartProductSerializer(serializers.ModelSerializer):
    """Сериализатор добавления продукта в корзину"""
    quantity = serializers.IntegerField(validators=[QuantityValidator()])
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = CartProduct
        fields = ['product', 'quantity', 'price', 'total_price', 'user']
        validators = [ProductValidator()]


class CartProductUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор изменения количества продукта в корзине"""
    quantity = serializers.IntegerField(validators=[QuantityValidator()])

    class Meta:
        model = CartProduct
        fields = '__all__'
        read_only_fields = ['product', 'user', 'price', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор корзины"""
    products_cart = CartProductSerializer(source='cartproduct_set', many=True)
    total_quantity = SerializerMethodField()
    total_cost = SerializerMethodField()

    class Meta:
        model = User
        fields = ['products_cart', 'total_quantity', 'total_cost']

    @staticmethod
    def get_total_quantity(obj):
        """Метод возвращает общее количество продуктов в корзине"""
        total_quantity = obj.cartproduct_set.aggregate(total_quantity=Sum('quantity'))
        return total_quantity['total_quantity']

    @staticmethod
    def get_total_cost(obj):
        """Метод возвращает общую стоимость продуктов в корзине"""
        total_cost = obj.cartproduct_set.aggregate(total_cost=Sum('total_price'))
        return total_cost['total_cost']
