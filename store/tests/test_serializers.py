from datetime import datetime
from collections import OrderedDict

from django.test import TestCase
from django.contrib.auth.models import User

from store.models import (
    Product, Price, Order, OrderProducts)


from store.serializers import (
    ProductSerialization, PriceSerialization, OrderSerialization,
    ClientSerialization, OrderProductsSerialization)


class PriceSerializationTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name='Product 1', description='Description 1')
        self.price = Price.objects.create(price=2.42, product=self.product)

        self.serializer = PriceSerialization(self.price, many=False)

    def test_price_get(self):

        response = {
            'id': 1,
            'price': 2.42,
            'currency': 'BRL',
            'product': 1,
            'created_at': self.price.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        }

        self.assertEqual(self.serializer.data, response)


class ProductSerializationTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name='Product 1', description='Description 1')
        self.price = Price.objects.create(price=2.42, product=self.product)

        self.serializer = ProductSerialization(self.product, many=False)

    def test_create_product(self):

        response = {
            'id': 1,
            'name': 'Product 1',
            'description': 'Description 1',
            'highlighted': False,
            'created_at': self.product.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'price': 2.42,
            'currency': 'BRL'
            }
        self.assertEqual(self.serializer.data, response)


class ClientSerializationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='meinreno', email='gabriel@gabriel.com',
            password='top_secret', first_name='Gabriel', last_name='Renó')

        self.serializer = ClientSerialization(self.user, many=False)

    def test_create_client(self):

        response = {
            'id': 1,
            'username': 'meinreno',
            'first_name': 'Gabriel',
            'last_name': 'Renó',
            'email': 'gabriel@gabriel.com'}

        self.assertEqual(self.serializer.data, response)


class OrderSerializationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='meinreno', email='gabriel@gabriel.com',
            password='top_secret', first_name='Gabriel', last_name='Renó')

        self.product = Product.objects.create(
            name='Product 1', description='Description 1')
        Price.objects.create(price=2.42, product=self.product)

        self.product2 = Product.objects.create(
            name='Product 2', description='Description 2')
        Price.objects.create(price=2.42, product=self.product2)

        order_json = {
            "client": self.user.id,
            "order_products": [
                {
                    "product": self.product.id,
                    "quantity": 10
                },
                {
                    "product": self.product2.id,
                    "quantity": 10
                }
            ]
        }

        self.serializer = OrderSerialization(data=order_json, many=False)
        if self.serializer.is_valid():
            self.serializer.save()
        else:
            raise Exception('Serializer error')

    def test_create_order(self):

        response = {
            'id': 1,
            'client': 1,
            'created_at': self.serializer.data['created_at'],
            'order_products': [
                OrderedDict(
                    [
                        ('id', 1),
                        ('order', 1),
                        ('product', 1),
                        ('price', 2.42),
                        ('quantity', 10)
                    ]
                ),
                OrderedDict(
                    [
                        ('id', 2),
                        ('order', 1),
                        ('product', 2),
                        ('price', 2.42),
                        ('quantity', 10)])]
        }

        self.assertEqual(self.serializer.data, response)
