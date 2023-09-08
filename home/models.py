from django.db import models
import random
import string
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):   
    first_name = models.CharField(max_length=70, blank=True);
    middle_name = models.CharField(max_length=70, blank=True);
    last_name = models.CharField(max_length=70, blank=True);
    email = models.CharField(max_length=70, blank=True);
    phone = models.CharField(max_length=20);
    id_number = models.CharField(max_length=10);
    USER_NAME_FIELD = 'email'

    def __str__(self):
        return self.email

class Account(models.Model):   
    rad = ''.join(random.choices(string.digits, k=8))
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.IntegerField(default=rad)
    balance = models.IntegerField(default=0);

class Deposit(models.Model):   
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_deposited = models.IntegerField(default=0);
    date_of_deposit = models.DateTimeField(auto_now_add=True, blank=True,null=True)

class Withdraw(models.Model):   
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_withdrawn = models.IntegerField(default=0);
    transaction_cost = models.IntegerField(default=0);
    date_of_withdraw = models.DateTimeField(auto_now_add=True, blank=True,null=True)
