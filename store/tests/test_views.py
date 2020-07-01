from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from django.http import Http404

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from store.models import (
    Product, Price, Order, OrderProducts, Category)

from store.views import ProductView


class ProductViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='meinreno', email='gabriel@gabriel.com',
            password='top_secret', first_name='Gabriel', last_name='Renó', is_staff=True)
        self.factory = APIRequestFactory()
        self.view = ProductView.as_view()
        self.category = Category.objects.create(name='Prato')
        self.product = Product.objects.create(
            name='Product 1', description='Description 1', category=self.category)
        self.price = Price.objects.create(
            price=2.42, currency='BRL', product=self.product)

    def test_product_create(self):

        url = reverse('product')
        product_json = {
            "name": "Product Test",
            "description": "Product Description",
            "price":  2.42,
            "unit": "1 Porcao",
            "category": self.category.id
        }
        request = self.factory.post(url, product_json, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEquals(response.status_code, 201)

    def test_product_get(self):
        url = reverse('product-details', kwargs={'pk': self.product.id})

        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.product.id)
        expect_response = {
            'id': self.product.id,
            'name': self.product.name,
            'description': self.product.description,
            'highlighted': False,
            'created_at': self.product.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'price': self.product.price,
            'currency': self.product.currency,
            'unit': self.product.unit,
            'category': self.category.id,
            'photo': None
        }
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data, expect_response)

    def test_product_patch(self):
        url = reverse('product-details', kwargs={'pk': self.product.id})
        update_json = {
            'name': 'Update Name',
            'description': 'Update Description',
        }
        request = self.factory.patch(url, data=update_json, format='json')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.product.id)

        self.assertEquals(response.status_code, 204)

        request = self.factory.get(url)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.product.id)

        expect_response = {
            'id': self.product.id,
            'name': 'Update Name',
            'description': 'Update Description',
            'highlighted': False,
            'created_at': self.product.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'price': 2.42,
            'currency': 'BRL',
            'unit': '',
            'category': 1,
            'photo': None
        }

        self.assertEquals(response.data, expect_response)

    def test_product_delete(self):
        url = reverse('product-details', kwargs={'pk': self.product.id})

        request = self.factory.delete(url)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=self.product.id)

        self.assertEquals(response.status_code, 204)
