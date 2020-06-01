from django.contrib import admin

from store.models import Product, Price, Order, OrderProducts, Category, Client
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe

class OrderProductsInline(admin.StackedInline):
    model = OrderProducts
    extra = 0
    fields = ["product", "price", "quantity"]

  

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ["client"]
    inlines = [OrderProductsInline]

admin.site.register(Product)
admin.site.register(Price)
admin.site.register(Category)
admin.site.register(Client)

