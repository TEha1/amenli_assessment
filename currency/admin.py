from django.contrib import admin

from currency.models import UserCurrency


@admin.register(UserCurrency)
class UserCurrencyAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'from_currency_type',
        'to_currency_type',
        'times',
    ]
