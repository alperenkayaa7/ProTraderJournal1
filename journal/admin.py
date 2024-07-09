from django.contrib import admin
from .models import Account, Trade, Profile

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'account_balance', 'account_r', 'owner')

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'entry_price', 'close_price', 'quantity', 'trade_owner')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location', 'birth_date')
