from django.shortcuts import render, get_object_or_404

from .models import Product
import random
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login

from .forms import SignUpForm

def home(request):
    context = {'title': 'Home'}  # Include title in the context
    try:
        products = list(Product.objects.all())
        random.shuffle(products)  # Shuffle products
        displayed_products = products[:5]  # Select first 5
        context['displayed_products'] = displayed_products
        context['error'] = None
    except Exception as e:
        context['error'] = str(e)
        context['displayed_products'] = []

    # Make sure to adjust 'Techwave/home.html' to the correct path if necessary
    return render(request, 'Techwave/home.html', context)

def main (request):
    context = {'title': 'Main'}
    return render(request, 'techwave/main.html', context)

def login (request):
    context = {'title': 'Login'}
    return render(request, 'techwave/Login & Register/login.html')

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Logowanie użytkownika zaraz po rejestracji
            return redirect('main')  # Przekierowanie do strony głównej
    else:
        form = SignUpForm()
    return render(request, 'techwave/Login & Register/register.html', {'form': form})


def chek (request):
    context = {'title': 'Chek'}
    return render(request, 'techwave/check.html')

def logout (request):
    context = {'title': 'Logout'}
    return render(request, 'techwave/logout.html')
def login (request):
    context = {'title': 'Login'}
    return render(request, 'techwave/Login & Register/login.html')

def productsite(request):
    context = {'title': 'Productsite'}
    try:
        # Pobranie produktu o id 1 lub zwrócenie 404 jeśli nie istnieje
        product = get_object_or_404(Product, id=1)
        context['product'] = product
        context['error'] = None
    except Exception as e:
        context['error'] = str(e)
        context['product'] = None

    return render(request, 'techwave/productsite.html', context)