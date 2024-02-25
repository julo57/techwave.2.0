from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import FakePayment
from .models import Order   

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text=' Wymagane. Podaj ważny adres email.' , required=True )
                             

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ten adres email jest już zarejestrowany.")
        return email


class FakePaymentForm(forms.ModelForm):
    class Meta:
        model = FakePayment
        fields = ['name', 'last_name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Imię'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nazwisko'}),
            'email': forms.HiddenInput(),
            'phone': forms.TextInput(attrs={'placeholder': 'Telefon'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'total_price', 'quantity', 'product_name']
        widgets = {
            'user': forms.HiddenInput(),
            'total_price': forms.HiddenInput(),
            'quantity': forms.HiddenInput(),
            
            'product_name': forms.HiddenInput(),
        }