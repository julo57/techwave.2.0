from django.contrib import admin
from .models import Product

from .models import CartItem
from .models import FakePayment

admin.site.register(Product)

admin.site.register(CartItem)
admin.site.register(FakePayment)