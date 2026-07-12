from django.shortcuts import render,redirect 
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from models import *


def login(request):
    if request.method == 'POST':
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        
        login_user = user.objects.filter(contact=contact).first()

        if login_user is not None and check_password(password, login_user.password):

            # SESSION SET
            request.session['email'] = login_user.email

            #  Redirect based on role
            if login_user.role == 'Farmer':
                login_user.is_active = True
                login_user.save()
                return redirect('farmer_home')
            elif login_user.role == 'Buyer':
                login_user.is_active = True
                login_user.save()
                return redirect('buyer_home')
            else:
                return redirect('home')

        else:
            messages.error(request, 'Invalid Contact number or password')
            return redirect('login')
            
    return render(request, "farmer/login.html")

def check_login(allowed_roles):
    def decorator(view_function):
        def wrapper(request, *args, **kwargs):
            if "email" in request.session:
                try:
                    login_user = user.objects.get(email=request.session['email'])
                    request.uid = login_user

                    #  Role check
                    if login_user.role not in allowed_roles:
                        messages.error(request, "Access Denied")
                        return redirect('login')

                    return view_function(request, *args, **kwargs)

                except user.DoesNotExist:
                    return redirect('login')

            return redirect('login')
        return wrapper
    return decorator


def index(request):
    return render(request, 'admin/index.html')

def assets(request):
    return render(request, 'admin/assets.html')

def allocations(request):
    return render(request, 'admin/allocations.html')

def bookings(request):
    return render(request, 'admin/bookings.html')

def transfers(request):
    return render(request, 'admin/transfers.html')
