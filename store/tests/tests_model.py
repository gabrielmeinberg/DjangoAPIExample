from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.http import Http404
from django.db.models.query import QuerySet

from store.models import Category, Order, OrderProducts, Price, Product


class ProductTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Prato')
        self.product = Product.objects.create(
            name='Product 1', description='Description 1', category=self.category)
        self.price = Price.objects.create(price=2.42, product=self.product)

    def test_classificacao_get(self):
        """ Create Product correctly """

        self.assertEqual(self.product.name, 'Product 1')
        self.assertEqual(self.product.description, 'Description 1')

    def test_get_price(self):
        """ Get Price from Product """

        self.assertEqual(self.product.price, 2.42)

    def test_get_price_instance(self):
        """ Get Price Instance """

        self.assertEqual(self.product.price_instance, self.price)


class PriceTestCase(TestCase):

    def setUp(self):

        self.category = Category.objects.create(name='Prato')
        self.product = Product.objects.create(
            name='Product 1', description='Description 1', category=self.category)
        self.price = Price.objects.create(price=2.42, product=self.product)

    def test_get_price(self):
        """ Test Create Price """

        self.assertEqual(self.price.price, 2.42)


class OrderTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='meinreno', email='gabriel@gabriel.com',
            password='top_secret')

        self.order = Order.objects.create(client=self.user)

    def test_get_order(self):
        """ Test Create Order """

        self.assertEqual(self.order.client, self.user)


class OrderProductsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='meinreno', email='gabriel@gabriel.com',
            password='top_secret')

        self.order = Order.objects.create(client=self.user)

        self.category = Category.objects.create(name='Prato')
        self.product = Product.objects.create(
            name='Product 1', description='Description 1', category=self.category)
        self.price = Price.objects.create(price=2.42, product=self.product)

        self.order_products = OrderProducts.objects.create(
            order=self.order,
            product=self.product,
            price=self.price,
            quantity=20)

    def test_create_order_products(self):
        self.assertEqual(self.order_products.order, self.order)
        self.assertEqual(self.order_products.product, self.product)
        self.assertEqual(self.order_products.price, self.price)
        self.assertEqual(self.order_products.quantity, 20)
