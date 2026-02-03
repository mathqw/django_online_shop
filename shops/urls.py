from django.urls import path
from .views import add_product, my_products
from . import views

urlpatterns = [
    path('add/', add_product, name='add_product'),
    path('my/', my_products, name='my_products'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('toggle/<int:product_id>/', views.toggle_product_active, name='toggle_product'),
]