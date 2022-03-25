from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('main:main_category', args=[self.slug])

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Brand(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = AutoSlugField(max_length=200, db_index=True, populate_from='name')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, related_name='brands', on_delete=models.CASCADE, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount = models.BooleanField(default=False)
    sale = models.FloatField(default=1)
    country = models.CharField(max_length=50, db_index=True)
    description = models.TextField(blank=True)
    full_description = models.TextField(blank=True)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    rating = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse ('main:product_detail', args=[self.id, self.slug])

    class Meta:
        ordering=('name',)
        index_together = (('id','slug'),)


class Profile(models.Model):
    adress = models.TextField(blank=True, null=True)
    phone = models.IntegerField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse ('main:profile', args=[self.user.id])


class Rating(models.Model):
    rating  = models.PositiveIntegerField()
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_rating')


class Image(models.Model):
    img = models.ImageField(upload_to='product/%Y/%m/%d')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_image')


class Order(models.Model):
    CHOICES_PAYMENT = (
        ('Наличные','Наличные при получении'),
        ('Оплата картой', 'Оплата картой'),
    )

    CHOICES_DELIVERY = (
        ('Самовывоз', 'Самовывоз'),
        ('Курьер', 'Курьер'),
        ('Почта', 'Почта'),
    )

    CHOICES_STATUS = (
        ('Принято в обработку', 'Принято в обработку'),
        ('Упакован и отправлен', 'Упакован и отправлен'),
        ('Доставлен покупателю', 'Доставлен покупателю'),
        ('Ожидание поступления товара', 'Ожидание поступления товара'),
        ('Отменен', 'Отменен'),
    )

    data_order = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField('Product', verbose_name='Товар')
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Покупатель')
    status = models.CharField(max_length=50, default='Принято в обработку', choices=CHOICES_STATUS, verbose_name='Статус заказа')
    total = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Итого')
    payment = models.CharField(max_length=50, choices=CHOICES_PAYMENT, verbose_name='Способ оплаты')
    delivery = models.CharField(max_length=50, choices=CHOICES_DELIVERY, verbose_name='Способ доставки')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    adress = models.TextField(null=True, verbose_name='Адрес')
    phone = models.CharField(null=True, max_length=13, verbose_name='Телефон')

    def get_absolute_url(self):
        return reverse ('main:order_details', args=[self.id])

