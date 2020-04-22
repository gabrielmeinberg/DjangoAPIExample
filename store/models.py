from django.contrib.auth.models import User
from django.db import models



class Product(models.Model):

    name = models.CharField(max_length=120)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'product_table'
        managed = True
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    @property
    def price(self):
        price_get = self.price_set.filter(
            product=self).order_by('created_at').last()
        if price_get:
            return price_get.price
        return None

    @property
    def price_instance(self):
        price_get = self.price_set.filter(
            product=self).order_by('created_at').last()
        return price_get


class Price(models.Model):
    price = models.FloatField()
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
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        pass

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
        pass

    class Meta:
        db_table = 'order_products_table'
        managed = True
        verbose_name = 'OrderProducts'
        verbose_name_plural = 'OrderProducts'
