from django.db import models

# Create your models here.
from users.models import Shop_Users

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    owner = models.ForeignKey(
        Shop_Users,
        on_delete=models.CASCADE,
        related_name='products'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)

    image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.owner.name})"
    
