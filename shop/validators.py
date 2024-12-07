from rest_framework.serializers import ValidationError

from shop.models import CartProduct


class QuantityValidator:

    def __call__(self, value):
        if value <= 0:
            raise ValidationError('Количество должно быть больше 0.')


class ProductValidator:

    def __call__(self, value):
        if CartProduct.objects.filter(
                user=dict(value).get('user'), product=dict(value).get('product')
        ).exists():
            raise ValidationError("Продукт уже есть в корзине")
