from django.http import Http404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from store.models import Product, Price, Order, Category, Client
from store.serializers import (
    ProductSerialization, PriceSerialization, OrderSerialization,
    UserSerialization, CategorySerialization, ClientSerialization)


class ProductView(APIView):

    def post(self, request, format=None) -> Response:

        serializers = ProductSerialization(data=request.data, many=False)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk: int = None, format=None) -> Response:

        if pk:
            try:
                product = Product.objects.get(id=pk)
                serializer = ProductSerialization(product, many=False)
            except:
                raise Http404
        else:
            products = Product.objects.all()
            serializer = ProductSerialization(products, many=True)

        return Response(serializer.data)

    def patch(self, request, pk: int, format=None) -> Response:
        try:
            product = Product.objects.get(id=pk)
        except:
            raise Http404

        serializer = ProductSerialization(
            product, data=request.data, partial=True, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: int, format=None) -> Response:

        try:
            Product.objects.get(id=pk).delete()
        except:
            raise Http404

        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderView(APIView):
    def post(self, request, format=None) -> Response:
        serializers = OrderSerialization(data=request.data, many=False)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk: int = None, format=None) -> Response:
        try:
            if pk:
                order = Order.objects.get(id=pk)
                serializer = OrderSerialization(order, many=False)
            else:
                orders = Order.objects.order_by('-created_at')
                serializer = OrderSerialization(orders, many=True)
        except:
            raise Http404

        return Response(serializer.data)

    def delete(self, request, pk: int, format=None) -> Response:
        try:
            Order.objects.get(id=pk).delete()
        except:
            raise Http404

        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientView(APIView):
    def post(self, request, format=None) -> Response:
        serializers = UserSerialization(data=request.data, many=False)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk: int, format=None) -> Response:
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerialization(user, many=False)
        except:
            raise Http404

        return Response(serializer.data)

    def patch(self, request, pk: int, format=None) -> Response:
        try:
            client = Client.objects.get(id=pk)
        except:
            raise Http404

        serializer = ClientSerialization(
            client, data=request.data, partial=True, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)


class PriceView(APIView):
    def post(self, request, format=None) -> Response:
        serializers = PriceSerialization(data=request.data, many=False)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryView(APIView):
    def post(self, request, format=None) -> Response:
        serializers = CategorySerialization(data=request.data, many=False)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None) -> Response:
        categories = Category.objects.all()
        serializer = CategorySerialization(categories, many=True)

        return Response(serializer.data)
        