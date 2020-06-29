from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models


def image_name(instance, filename):
    ext = filename.split('.')[-1]

    return f'images/{uuid4()}.{ext}'


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50)
    address = models.TextField()

    def __str__(self):
        return f'{self.user}'

    class Meta:
        db_table = 'client_table'
        managed = True
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'ID: {self.id} Name: {self.name}'

    class Meta:
        db_table = 'category_table'
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Product(models.Model):

    name = models.CharField(max_length=120)
    description = models.TextField()
    highlighted = models.BooleanField(default=False)
    unit = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    category = models.ForeignKey(
        Category, related_name='product_category', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=image_name)

    def __str__(self):
        return f'ID: {self.id} Name: {self.name}'

    class Meta:
        db_table = 'product_table'
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']

    @property
    def price_instance(self):
        price_get = self.price_set.filter(
            product=self).order_by('created_at').last()
        return price_get

    @property
    def price(self):
        price_get = self.price_instance
        if price_get:
            return price_get.price
        return None

    @property
    def currency(self):
        price_get = self.price_instance
        if price_get:
            return price_get.currency
        return None


class Price(models.Model):
    price = models.FloatField()
    currency = models.CharField(max_length=3, default='BRL')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'ID: {self.id} Product ID: {self.product.id} Price: {self.price}'

    class Meta:
        db_table = 'price_table'
        managed = True
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'


class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    type_payment = models.CharField(max_length=50)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'ID: {self.id} Client: {self.client}'

    class Meta:
        db_table = 'order_table'
        managed = True
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderProducts(models.Model):
    order = models.ForeignKey(
        Order, related_name='order_products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.ForeignKey(Price, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'Order: {self.order}'

    class Meta:
        db_table = 'order_products_table'
        managed = True
        verbose_name = 'OrderProducts'
        verbose_name_plural = 'OrderProducts'
