from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Shop_Users


@receiver(post_save, sender=Shop_Users)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        from payments.models import Wallet
        Wallet.objects.create(user=instance)