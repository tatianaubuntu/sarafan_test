from django.db import models
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from pilkit.processors import ResizeToFill
from smart_selects.db_fields import ChainedForeignKey
from config.settings import AUTH_USER_MODEL

NULLABLE = {'null': True, 'blank': True}


class Category(MPTTModel):
    """Класс, описывающий информацию о категории, подкатегории"""
    title = models.CharField(max_length=150,
                             verbose_name='название')
    image = models.ImageField(upload_to='image/',
                              verbose_name='изображение',
                              **NULLABLE)
    slug = models.SlugField(unique=True,
                            verbose_name='slug')
    parent_category = TreeForeignKey('self',
                                     on_delete=models.SET_NULL,
                                     **NULLABLE,
                                     verbose_name='Родительская категория',
                                     related_name='children')

    def save(self, *args, **kwargs):
        """Метод автоматически создает slug по названию"""
        if not self.id and not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class MPTTMeta:
        parent_attr = 'parent_category'
        order_insertion_by = ['title']

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    """Класс, описывающий информацию о продукте"""
    title = models.CharField(max_length=150,
                             verbose_name='название')
    slug = models.SlugField(unique=True,
                            verbose_name='slug')
    price = models.DecimalField(max_digits=12,
                                decimal_places=2,
                                default=0,
                                verbose_name='цена')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 **NULLABLE,
                                 verbose_name='категория')
    subcategory = ChainedForeignKey(Category,
                                    chained_field="category",
                                    chained_model_field="parent_category",
                                    show_all=False,
                                    auto_choose=True,
                                    sort=True,
                                    on_delete=models.SET_NULL,
                                    **NULLABLE,
                                    verbose_name='подкатегория',
                                    related_name='subcategory')
    image = models.ImageField(upload_to='image/',
                              verbose_name='изображение',
                              **NULLABLE)
    image_1 = ImageSpecField(source='image',
                             processors=[ResizeToFill(500, 400)],
                             options={'quality': 60},
                             )
    image_2 = ImageSpecField(source='image',
                             processors=[ResizeToFill(400, 300)],
                             options={'quality': 60})

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class CartProduct(models.Model):
    """Класс, описывающий информацию о продукте в корзине"""
    user = models.ForeignKey(AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name="пользователь",
                             **NULLABLE)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='продукт')
    quantity = models.PositiveIntegerField(verbose_name='количество',
                                           default=1)
    price = models.DecimalField(max_digits=12,
                                decimal_places=2,
                                default=0,
                                verbose_name='цена',
                                **NULLABLE)
    total_price = models.DecimalField(max_digits=12,
                                      decimal_places=2,
                                      default=0,
                                      verbose_name='стоимость',
                                      **NULLABLE)

    def __str__(self):
        return f'{self.product}'

    class Meta:
        verbose_name = 'продукт в корзине'
        verbose_name_plural = 'продукты в корзине'
