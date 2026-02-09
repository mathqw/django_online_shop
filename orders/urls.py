from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('', views.seller_orders, name='seller_orders'),
    path('accept/<int:order_id>/',
         views.accept_order,
         name='accept_order'),
    path('complete/<int:order_id>/',
         views.complete_order,
         name='complete_order'),
]
