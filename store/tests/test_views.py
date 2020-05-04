from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from django.http import Http404

from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from store.models import (
    Product, Price, Order, OrderProducts)

from store.views import ProductView


class ProductViewTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ProductView.as_view()
        self.product = Product.objects.create(
            name='Product 1', description='Description 1')
        self.price = Price.objects.create(price=2.42, currency='BRL', product=self.product)

    def test_product_create(self):

        url = reverse('product')
        product_json = {
            "name": "Product Test",
            "description": "Product Description",
            "price":  2.42,
            "unit": "1 Porcao"
        }
        request = self.factory.post(url, product_json, format='json')
        response = self.view(request)
        self.assertEquals(response.status_code, 201)

    def test_product_get(self):
        url = reverse('product-details', kwargs={'pk': self.product.id})

        request = self.factory.get(url)
        response = self.view(request, pk=self.product.id)
        expect_response = {
            'id': self.product.id,
            'name': self.product.name,
            'description': self.product.description,
            'highlighted': False,
            'created_at': self.product.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'price': self.product.price,
            'currency': self.product.currency,
            'unit': self.product.unit
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

        response = self.view(request, pk=self.product.id)

        self.assertEquals(response.status_code, 204)

        request = self.factory.get(url)
        response = self.view(request, pk=self.product.id)

        expect_response = {
            'id': self.product.id,
            'name': 'Update Name',
            'description': 'Update Description',
            'highlighted': False,
            'created_at': self.product.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'price': 2.42,
            'currency': 'BRL',
            'unit': ''
        }
        self.assertEquals(response.data, expect_response)

    def test_product_delete(self):
        url = reverse('product-details', kwargs={'pk': self.product.id})

        request = self.factory.delete(url)

        response = self.view(request, pk=self.product.id)

        self.assertEquals(response.status_code, 204)

