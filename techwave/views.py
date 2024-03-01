from django.shortcuts import render, get_object_or_404

from .models import Product , Cart, CartItem, FakePayment , Order
import random
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.http import HttpResponse
from .forms import OrderForm
from .forms import FakePaymentForm
from .forms import SignUpForm
from .forms import CommentForm
from .models import Product, Cart, CartItem, FakePayment, Order
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem
from django.contrib import messages


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
    context = {'title': 'korwa', 'error': 'sss'}
    return render(request, 'techwave/check.html',context)

def logout (request):
    context = {'title': 'Logout'}
    return render(request, 'techwave/logout.html')
def login (request):
    context = {'title': 'Login'}
    return render(request, 'techwave/Login & Register/login.html')

def productsite(request):
    product = get_object_or_404(Product, id=10)  # Załóżmy, że to jest ID produktu, którego strona jest wyświetlana.
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
            messages.success(request, 'Komentarz został dodany.')  # Dodanie wiadomości o sukcesie
            return redirect(request.path_info)  # Przekierowuje na tę samą stronę, co zapobiega ponownemu przesłaniu formularza przy odświeżeniu
    else:
        form = CommentForm()

    comments = product.comments_set.all()  # Pobieranie wszystkich komentarzy dla danego produktu
    context = {
        'title': 'Productsite',
        'product': product,
        'form': form,
        'comments': comments,  # Dodajemy komentarze do kontekstu, aby można było je wyświetlić na stronie
    }

    return render(request, 'techwave/productsite.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem
from django.contrib import messages

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    try:
        # Spróbuj znaleźć istniejący element koszyka dla tego produktu
        cart_item = CartItem.objects.get(cart=cart, product=product)
        # Jeśli element koszyka już istnieje, zwiększ jego ilość o 1
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Ilość produktu {product.name} w koszyku została zwiększona.')
    except CartItem.DoesNotExist:
        # Jeśli element koszyka nie istnieje, stwórz nowy
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        messages.success(request, f'{product.name} został dodany do koszyka.')

    return redirect('home')  # Przekierowanie na stronę główną lub gdziekolwiek indziej


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






def payment(request):
    if request.method == 'POST':
        form = FakePaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.email = request.user.email
            payment.save()
            # Poprawka: użyj utworzonej instancji płatności do pobrania jej ID
            fake_payment_id = payment.id
            return redirect('summation', FakePayment_id=fake_payment_id)
    else:
        form = FakePaymentForm()

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'techwave/Payments/payment.html', {'cart_items': cart_items, 
                                                              'total_price': total_price, 'form': form})


def summation(request, FakePayment_id):
    
    payment = FakePayment.objects.get(id=FakePayment_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    context = {
        'payment': payment, 
        'title': 'Summation', 
        'summation_id': FakePayment_id, 
        'cart_items': cart_items, 
        'total_price': total_price
    }
    
    return render(request, 'techwave/Payments/summation.html', context)

def order(request):
    user = request.user
    total_price = request.POST.get('total_price')
    quantity = request.POST.get('quantity')
   
    product_name = request.POST.get('product_name')

    # Tworzenie nowego zamówienia
    Order.objects.create(user=user, total_price=total_price, quantity=quantity , product_name=product_name)

    # Przekieruj użytkownika do strony potwierdzenia lub gdziekolwiek indziej
    return redirect('profile')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('main')
    
    # Pobierz zamówienia dla zalogowanego użytkownika
    zamowienia = Order.objects.filter(user=request.user)  
    context = {'title': 'Profile', 'zamowienia': zamowienia}
    return render(request, 'techwave/profile.html', context)


def main(request):
    products = Product.objects.all()  # Pobierz wszystkie produkty z bazy danych
    return render(request, 'techwave/main.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    comments = product.comments_set.all()
    form = CommentForm()
    context = {
        'product': product,
        'comments': comments,
        'form': form,
    }
    return render(request, 'techwave/productsite.html', context)
