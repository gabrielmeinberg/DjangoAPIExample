from datetime import datetime
from collections import OrderedDict

from django.test import TestCase
from django.contrib.auth.models import User

from store.models import Category, Order, OrderProducts, Price, Product, Client


from store.serializers import (
    ProductSerialization, PriceSerialization, OrderSerialization,
    UserSerialization, OrderProductsSerialization)


class PriceSerializationTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Prato')
        self.product = Product.objects.create(
            name='Product 1', description='Description 1', category=self.category)
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
        self.category = Category.objects.create(name='Prato')
        self.product = Product.objects.create(
            name='Product 1', description='Description 1', category=self.category)
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
            'currency': 'BRL',
            'unit': '',
            'category': self.category.id,
            'photo': None
        }

        self.assertEqual(self.serializer.data, response)


class UserSerializationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='meinreno', email='gabriel@gabriel.com',
            password='top_secret', first_name='Gabriel', last_name='Renó')

        Client.objects.create(
            user=self.user, address="Av. Teste, 97", phone="99999-9999")

        self.serializer = UserSerialization(self.user, many=False)

    def test_create_client(self):

        response = {
            'id': 1,
            'username': 'meinreno',
            'first_name': 'Gabriel',
            'last_name': 'Renó',
            'email': 'gabriel@gabriel.com',
            'client_set': [
                {
                    'phone': '99999-9999',
                    'address': 'Av. Teste, 97',
                    'id': 1
                }]}

        self.assertEqual(self.serializer.data, response)


class OrderSerializationTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='meinreno', email='gabriel@gabriel.com',
            password='top_secret', first_name='Gabriel', last_name='Renó')

        self.client = Client.objects.create(
            user=self.user, phone='1199999-9999', address='Rua Teste')

        self.category = Category.objects.create(name='Prato')
        self.product = Product.objects.create(
            name='Product 1', description='Description 1', category=self.category)
        Price.objects.create(price=2.42, product=self.product)

        self.product2 = Product.objects.create(
            name='Product 2', description='Description 2', category=self.category)
        Price.objects.create(price=2.42, product=self.product2)

        order_json = {
            "client": self.user.id,
            "type_payment": "Cartão",
            "order_products": [
                {
                    "product": self.product.id,
                    "quantity": 10
                },

                {
                    "product": self.product2.id,
                    "quantity": 20
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
                        ('quantity', 20)])],
            'type_payment': 'Cartão',
            'address': 'Rua Teste'
        }

        self.assertEqual(self.serializer.data, response)
