from django import forms

from shop.models import Category


class ProductAdminForm(forms.ModelForm):
    """Форма административной панели выбора категорий"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(level=0)
