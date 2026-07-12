from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from models import *
# Create your views here.

def login(request):
    if request.method == 'POST':
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        
        login_user = user.objects.filter(contact=contact).first()

        if login_user is not None and check_password(password, login_user.password):

            # Buyer verification check
            # if user.role == 'Buyer':
            #     if not hasattr(user, 'buyer') or not user.buyer.is_verified:
            #         messages.error(request, 'Sorry you are not verified yet')
            #         return redirect('login')

            # SESSION SET
            request.session['email'] = login_user.email

            #  Redirect based on role
            if login_user.role == 'admin':
                login_user.is_active = True
                login_user.save()
                return redirect('farmer_home')
            elif login_user.role == 'manager':
                login_user.is_active = True
                login_user.save()
                return redirect('buyer_home')
            elif login_user.role == 'dept_head':
                login_user.is_active = True
                login_user.save()
                return redirect('buyer_home')
            elif login_user.role == 'employee':
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


                    #  Buyer verification
                    # if login_user.role == 'Buyer':
                    #     if not hasattr(login_user, 'buyer') or not login_user.buyer.is_verified:
                    #         messages.error(request, "Not verified")
                    #         return redirect('login')

                    return view_function(request, *args, **kwargs)

                except user.DoesNotExist:
                    return redirect('login')

            return redirect('login')
        return wrapper
    return decorator

