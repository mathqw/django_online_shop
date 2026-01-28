from django.contrib import admin

# Register your models here.
from .models import Wallet, Card, Transaction


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'currency', 'created_at')
    search_fields = ('user__name',)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('card_name', 'user', 'card_type', 'is_active')
    list_filter = ('card_type', 'is_active')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'amount', 'status', 'created_at')
    list_filter = ('status', 'transaction_type')