from django.contrib import admin

from store.models import Product, Price, Order

admin.site.register(Product)
admin.site.register(Price)
admin.site.register(Order)
