from django.contrib import admin
from .models import User, Account, Deposit, Withdraw

# Register your models here.
admin.site.register(User)
admin.site.register(Account)
admin.site.register(Deposit)
admin.site.register(Withdraw)