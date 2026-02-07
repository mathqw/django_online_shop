from django.db import models


class Wallet(models.Model):
    user = models.OneToOneField(
        'users.Shop_Users',  # <-- строковая ссылка вместо импорта
        on_delete=models.CASCADE,
        related_name='wallet'
    )
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='UAH')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} | {self.balance}"


class Card(models.Model):
    CARD_TYPES = (
        ('visa', 'VISA'),
        ('mastercard', 'MasterCard'),
        ('fake', 'Fake'),
    )

    user = models.ForeignKey(
        'users.Shop_Users',  
        on_delete=models.CASCADE,
        related_name='cards'
    )
    card_name = models.CharField(max_length=100)
    last4 = models.CharField(max_length=4)
    card_type = models.CharField(max_length=20, choices=CARD_TYPES)
    balance = models.DecimalField(
        max_digits=10,     
        decimal_places=2,  
        default=0
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_name} ****{self.last4}"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('topup', 'Top Up'),
        ('payment', 'Payment'),
        ('refund', 'Refund'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(
        'users.Shop_Users',  # <-- строковая ссылка
        on_delete=models.CASCADE
    )
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE
    )

    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    source = models.CharField(max_length=50, null=True, blank=True)
    source_id = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} {self.amount}"