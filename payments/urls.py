from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path('add/', views.add_card, name='add_card'),
]