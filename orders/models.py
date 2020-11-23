from django.db import models
from django.conf import settings

from shop.models import Product

class Order(models.Model):
    STATUS_CHOICES = (
    ('Прийнятий', 'Прийнятий'),
    ('В обробці', 'В обробці'),
    ('Виконаний', 'Виконаний'),
    ('Відмінений', 'Відмінений'),
    ('Small', 'Small'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, default='', blank = True)
    first_name = models.CharField(max_length=255, verbose_name = 'Ім\'я')
    last_name = models.CharField(max_length=255, verbose_name = 'Прізвище')
    email = models.EmailField()
    address = models.CharField(max_length=250, verbose_name = 'Адреса')
    postal_code = models.CharField(max_length=255, verbose_name = 'Поштовий індекс', blank = True)
    city = models.CharField(max_length=100, verbose_name = 'Місто')
    created = models.DateTimeField(auto_now_add=True, verbose_name = 'Створено')
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Оновлено')
    paid = models.BooleanField(default=False, verbose_name = 'Оплачено')
    status = models.CharField(max_length=10,choices=STATUS_CHOICES, default='Прийнятий', verbose_name = 'Статус')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказамовлення'
        verbose_name_plural = 'Заказамовлення'

    def __str__(self):
        return 'Замовлення №{}'.format(self.id)
        return self.get_status_display()

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name = 'Ціна')
    quantity = models.PositiveIntegerField(default=1, verbose_name = 'Кількість')

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
