from django.shortcuts import render
from .models import Product
import random

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

def base (request):
    context = {'title': 'Base'}
    return render(request, 'Techwave/base.html', context)

def login (request):
    context = {'title': 'Login'}
    return render(request, 'techwave/Login & Register/login.html')

def register (request):
    context = {'title': 'Register'}
    return render(request, 'techwave/Login & Register/register.html')
