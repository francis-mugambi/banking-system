from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='index'),    
    path('login/', views.login, name='login'),
    path('create-account/', views.createAccount, name='create-account'),
    path('profile/', views.profile, name='profile'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transactions/', views.transactions, name='transactions'),
    path('balance/', views.balance, name='balance'),
    
]