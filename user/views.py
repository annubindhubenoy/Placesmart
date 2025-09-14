from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


def signup_view(request):
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validation
        if not first_name or not last_name or not email or not password1 or not password2:
            messages.error(request, "All fields are required")
            return redirect('signup')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('signup')

        # Create user
        user = User.objects.create_user(
            username=email,  # Using email as username
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1
        )
        login(request, user)
        return redirect('aptitudetest')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            username = None

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('selection_page')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')

    return render(request, 'login.html')


def home_view(request):
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('home')

def aptitudetest_view(request):
    return render(request, 'aptitudetest.html')

def selection_page(request):
    return render(request, 'selection_page.html')




# Create your views here.
