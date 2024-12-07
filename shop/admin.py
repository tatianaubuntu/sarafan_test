from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin

from shop.forms import ProductAdminForm
from shop.models import Category, Product, CartProduct


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin, admin.ModelAdmin):
    """Административная панель категорий, подкатегорий"""
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Административная панель продуктов"""
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('id', 'title', 'price', 'category', 'subcategory', 'image', 'image_1_link', 'image_2_link')
    form = ProductAdminForm

    @admin.display(description='Миниатюра_1')
    def image_1_link(self, obj):
        """Метод добавляет ссылку на миниатюру 1"""
        if obj.image_1:
            return format_html('<a href="{}">{}</a>', obj.image_1.url, obj.image_1)

    @admin.display(description='Миниатюра_2')
    def image_2_link(self, obj):
        """Метод добавляет ссылку на миниатюру 2"""
        if obj.image_2:
            return format_html('<a href="{}">{}</a>', obj.image_2.url, obj.image_2)


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    """Административная панель продуктов в корзине"""
    list_display = ('id', 'product', )
