from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length = 255, verbose_name = 'Назва')
    slug = models.SlugField(max_length = 255)

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return self.name

class Characteristic(models.Model):
    admin_name = models.CharField(max_length = 255, verbose_name = 'Назва в панелі-адміністратора', default = '')
    filter_name = models.CharField(max_length = 255, verbose_name = 'Назва для фільтру', default = '', blank = True)
    name = models.CharField(max_length = 255, verbose_name = 'Характеристика')
    value = models.CharField(max_length = 255, verbose_name = 'Значення')

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

    def __str__(self):
        return self.admin_name

class Product(models.Model):
    STATUS_CHOICES = (
    ('draft', 'В обробці'),
    ('published', 'Опубліковано'),
    )
    category = models.ForeignKey(Category, on_delete = models.CASCADE, verbose_name = 'Категорія')
    name = models.CharField(max_length = 255, verbose_name = 'Назва')
    slug = models.SlugField(max_length = 255, default = '')
    image = models.ImageField(upload_to='images/products/',blank = True)
    description = models.TextField(verbose_name = 'Опис', blank = True)
    characteristics = models.ManyToManyField(Characteristic)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    publish = models.DateTimeField(editable=True, auto_now_add=True, verbose_name = 'Опубліковано')
    updated = models.DateTimeField(editable=True, auto_now=True, verbose_name = 'Оновлено')
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft', verbose_name = 'Статус')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'

    def __str__(self):
        return self.name

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name = 'Товар', related_name = 'comments')
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = 'Користувач')
    body = models.TextField(max_length = 500)
    created = models.DateTimeField(auto_now_add = True, verbose_name = 'Додано')
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Оновлено')
    active = models.BooleanField(default=True, verbose_name = 'Відображати?')

    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
        ordering = ('-created',)

    def __str__(self):
        return 'Написав {} до {}'.format(self.user, self.product)
