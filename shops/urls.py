from django.urls import path
from .views import add_product, my_products

urlpatterns = [
    path('add/', add_product, name='add_product'),
    path('my/', my_products, name='my_products'),
]