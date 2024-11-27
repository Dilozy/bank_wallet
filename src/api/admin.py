from django.contrib import admin

from .models import BankWallet, Transaction


admin.site.register(BankWallet)
admin.site.register(Transaction)
