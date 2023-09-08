from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import auth
from .models import Account, Deposit, Withdraw
# Create your views here.
def home(request, *args, **kwargs):
	return render(request, 'home/index.html')

def login(request, *args, **kwargs):
    if request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']

        check_email = User.objects.filter(email=email).exists()
        user = authenticate(request, username=email, password=password)
        
        if email =="":
            return render(request, 'home/login.html',{"msg1":"Fill the Email field"})

        if password =="":
            return render(request, 'home/login.html',{"msg1":"Fill the password field"})

        if check_email == False:
            return render(request, 'home/login.html',{"msg1":"The email does not exist in our database!"})

        if user is  None:
            return render(request, 'home/login.html',{"msg1":"Invalid Password!"})

        else:
            auth.login(request, user)			
            request.session['semail'] = email  
            return redirect('profile')
            
    else:
        return render(request, 'home/login.html')


def createAccount(request, *args, **kwargs):
    if request.method == 'POST':
        email = request.POST['email'].lower()
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        middle_name = request.POST['middle_name']
        password = request.POST['password']
        rpt_password = request.POST['rpt_password']

        email_confirm = User.objects.filter(email=email).exists()

        if email =="" or first_name=="" or last_name=="" or email=="":
            messages.info(request, " All the fields are required")	
            return redirect('create-account')

        if rpt_password != password:
            messages.info(request, "The passwords did not match!")	
            return redirect('create-account')			

        if email_confirm :
            messages.info(request, "A user with that email aready exists")	
            return redirect('create-account')

        if len(password) < 4 or len(password) > 15:
            messages.info(request, "A Password should have 4-15 characters!")	
            return redirect('create-account')	

        else:
            user =User.objects.create_user(username=email,first_name=first_name,last_name=last_name,middle_name=middle_name,email=email, password=password)
            
            acc = User.objects.get(email=email)
            account = Account.objects.create(owner=acc, balance=0)
            user.save()		
            account.save()	
            messages.info(request, "Account created successfully, please login!")	
            return redirect('login')
    
    else:
        return render(request, 'home/create_account.html')


def profile(request, *args, **kwargs):
    if request.method == 'POST':
        email = request.POST['email'].lower()
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']       
        id_number = request.POST['id_number']
        phone = request.POST['phone']

        if email =="" or first_name=="" or last_name=="" or email=="":
            messages.info(request, " All the fields are required")	
            return redirect('profile')	

        if len(id_number) != 8:
            messages.info(request, " A valid Id number should have 8 digits!")	
            return redirect('profile')	

        if len(phone) < 9 or len(phone) >13:
            messages.info(request, " A valid phone number should have 10 - 13 digits!")	
            return redirect('profile')	        

        else:
            entry = User.objects.get(email=request.user.email)
            entry.first_name = first_name
            entry.last_name = last_name	
            entry.middle_name = middle_name
            entry.email =email
            entry.phone = phone
            entry.id_number = id_number

            
            entry.save()
            messages.info(request, "Profile updated successfully.")	
            return redirect('profile')		
    
    else:
        account = Account.objects.get(id=request.user.id)
        user = User.objects.get(id=request.user.id)
        context = {
            'user':user,
            'account':account
        }
        return render(request, 'home/profile.html', context)


def deposit(request, *args, **kwargs):
    if request.method == 'POST':
        add_funds = int(request.POST['add_funds'])


        if add_funds =="":
            messages.info(request, " You did not enter any amount")	
            return redirect('deposit')	

        else:
            entry = Account.objects.get(owner=request.user.id)
            entry.balance = (entry.balance + add_funds)            
            entry.save()
            messages.info(request, f"You have deposited {add_funds} Ksh successfully.")	
            
            user = User.objects.get(email=request.user.email)
            depo = Deposit.objects.create(owner=user, amount_deposited=add_funds)
            depo.save()
            
            return redirect('deposit')		
    
    else:
	    return render(request, 'home/deposit.html')

def withdraw(request, *args, **kwargs):
    if request.method == 'POST':
        withdraw = int(request.POST['withdraw'])
        balance = Account.objects.get(owner=request.user.id)
        transaction_cost = 0
        if withdraw <= 100:
            transaction_cost = 0
        if withdraw >100 and withdraw <1000:
            transaction_cost = 10
        elif withdraw > 1000 and withdraw <2000:
            transaction_cost = 20
        elif withdraw >2000:
            transaction_cost = 30
        else:
            pass


        if withdraw =="":
            messages.info(request, " You did not enter any amount")	
            return redirect('withdraw')	

        if withdraw > balance.balance:
            messages.info(request, f" You do not have sufficient funds to withdraw {withdraw}! Your balance is {balance.balance}")	
            return redirect('withdraw')	

        else:
            entry = Account.objects.get(owner=request.user.id)
            entry.balance = (entry.balance - (withdraw + transaction_cost))            
            entry.save()
            messages.info(request, f"You have withdrawn {withdraw} Ksh successfully.")	 

            user = User.objects.get(email=request.user.email)
            withdraw = Withdraw.objects.create(owner=user, amount_withdrawn=withdraw, transaction_cost=transaction_cost)
            withdraw.save()
            
            return redirect('withdraw')		
    
    else:
	    return render(request, 'home/withdraw.html')

def balance(request, *args, **kwargs):
    balance = Account.objects.get(owner=request.user.id)
    context={
        'balance':balance
    }
    return render(request, 'home/balance.html', context)

def transactions(request, *args, **kwargs):
    deposit = Deposit.objects.all()
    withdraw = Withdraw.objects.all()
    context={
        'deposits':deposit,
        'withdraws':withdraw,
    }
    return render(request, 'home/transactions.html', context)