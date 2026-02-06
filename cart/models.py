# cart/models.py
from django.db import models
from users.models import Shop_Users
from shops.models import Product

class Cart(models.Model):
    user = models.OneToOneField(Shop_Users, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Кошик {self.user.name}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.title} x{self.quantity}"
