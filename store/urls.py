from django.urls import path
from store import views

urlpatterns = [
     path('product/', views.ProductView.as_view(), name='product'),
     path('product/details/<int:pk>/',
         views.ProductView.as_view(), name='product-details'),

     path('price/', views.PriceView.as_view(), name='price'),
     path('price/details/<int:pk>', views.PriceView.as_view(), name='price-details'),

     path('order/', views.OrderView.as_view(), name='price'),
     path('order/details/<int:pk>/',
         views.OrderView.as_view(), name='price-details'),

     path('client/', views.ClientView.as_view(), name='price'),
     path('client/details/',
         views.ClientView.as_view(), name='price-details'),

     path('category/', views.CategoryView.as_view(), name='category'),
]
