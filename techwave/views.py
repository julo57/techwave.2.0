from django.shortcuts import render, get_object_or_404

from .models import Product
import random
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .models import Cart, CartItem
from django.contrib import messages
from django.http import HttpResponse



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
        product = get_object_or_404(Product, id=3)
        context['product'] = product
        context['error'] = None
    except Exception as e:
        context['error'] = str(e)
        context['product'] = None

    return render(request, 'techwave/productsite.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'{product.name} został dodany do koszyka.')
        # Dodaj alert po dodaniu produktu do koszyka
        return HttpResponse('<script>alert("Product added to cart"); window.location.href = "/";</script>')
    return redirect('home')



def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    messages.success(request, 'Produkt został usunięty z koszyka.')
    return redirect('cart')


def cart(request):
    # Get the cart for the current user or create one if it doesn't exist
    cart, created = Cart.objects.get_or_create()
    
    # Retrieve all cart items for the current cart
    cart_items = cart.cartitem_set.all()
    
    # Calculate the total price of all items in the cart
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    return render(request, 'techwave/cart.html', {'cart_items': cart_items, 'total_price': total_price})


def profile(request):
    context = {'title': 'Profile'}
    return render(request, 'techwave/profile.html', context)    

