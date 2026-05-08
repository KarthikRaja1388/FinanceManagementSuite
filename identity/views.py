from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages

from identity.models import UserProfile


# Create your views here.
def index(request):
    return render(request, "identity/index.html")

def signup_user(request):

    if request.method == 'GET':
        return render(request, "identity/signup.html")

    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        print(first_name, last_name, email, password, confirm_password)

        if not all([first_name, last_name, email, password, confirm_password]):
            messages.warning(request, "Required fields can't be empty.")
            return render(request, "identity/signup.html")

        if User.objects.filter(username=email).exists():
            messages.warning(request, "Username already exists")
            return render(request, "identity/signup.html")

        if password != confirm_password:
            messages.warning(request, "Passwords does not match")
            return render(request, "identity/signup.html")
        try:
            with transaction.atomic():
                user = User.objects.create(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                user.set_password(password)
                user.save()

                UserProfile.objects.create(
                    user=user,
                    user_type="ADM",
                    account_owner=user,
                    is_admin = True,
                )

            messages.success(request, "Signup successful")
            return redirect('login_view')
        except Exception as e:
            messages.error(request, f"{e}")
            return render(request, "identity/signup.html")

    return render(request, "identity/signup.html")

def reset_password(request):
    pass

def authenticate_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            messages.error(request, "Invalid credentials")
            return redirect(request, "identity/login.html")

        return redirect('view_dashboard')

def logout_user(request):
    logout(request)
    return redirect('login_page')

def is_admin(request)->bool:
    pass



