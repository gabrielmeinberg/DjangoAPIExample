from django.contrib.auth.models import User, Group

from rest_framework import serializers

from store.models import (Product, Price, Order, OrderProducts, Category)


class PriceSerialization(serializers.ModelSerializer):

    class Meta:
        model = Price
        fields = ['id', 'price', 'currency', 'product', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductSerialization(serializers.ModelSerializer):
    price = serializers.FloatField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'highlighted', 'created_at', 'price', 'currency', 'unit', 'category']
        read_only_fields = ['id', 'created_at', 'currency']

    def create(self, validated_data):
        price_data = validated_data.pop('price')
        product = Product.objects.create(**validated_data)
        Price.objects.create(product=product, price=price_data)
        return product


class OrderProductsSerialization(serializers.ModelSerializer):
    price = serializers.SlugRelatedField(
        slug_field='price', many=False, read_only=True)

    class Meta:
        model = OrderProducts
        fields = ['id', 'order', 'product', 'price', 'quantity']
        read_only_fields = ['id', 'order', 'price']


class OrderSerialization(serializers.ModelSerializer):
    order_products = OrderProductsSerialization(many=True)

    class Meta:
        model = Order
        fields = ['id', 'client', 'created_at', 'order_products']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        orders_products_data = validated_data.pop('order_products')
        order = Order.objects.create(**validated_data)
        for order_products_data in orders_products_data:
            price = order_products_data['product'].price_instance

            OrderProducts.objects.create(
                order=order, price=price, **order_products_data)
        return order


class ClientSerialization(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'email', 'password']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        group, _ = Group.objects.get_or_create(name='clients')
        group.user_set.add(user)
        return user


class CategorySerialization(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']