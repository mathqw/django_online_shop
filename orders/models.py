# Create your models here.
from django.db import models
from users.models import Shop_Users
from shops.models import Product


class Order(models.Model):

    STATUS_CHOICES = [
        ('CART', 'У кошику'),
        ('PENDING', 'Очікує підтвердження'),
        ('ACCEPTED', 'Прийнято продавцем'),
        ('COMPLETED', 'Завершено'),
    ]

    buyer = models.ForeignKey(
        Shop_Users,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='CART'
    )

    def __str__(self):
        return f"Order #{self.id} - {self.buyer.name}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    seller = models.ForeignKey(
        Shop_Users,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.product.title} x{self.quantity}"
