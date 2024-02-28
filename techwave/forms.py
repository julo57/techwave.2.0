from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Product, Category

from .models import FakePayment
from .models import Order   
from .models import Comments

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control-material','id':'email', 'placeholder': ' ', 'autocomplete': 'off'})
    )

    # Przeniesienie definicji pól password1 i password2 poza Meta
    password1 = forms.CharField(
        
        widget=forms.PasswordInput(attrs={'class': 'form-control-material'}),
    )
    password2 = forms.CharField(
        
        widget=forms.PasswordInput(attrs={'class': 'form-control-material'}),
    )

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # Ukrywanie pomocniczych tekstów dla określonych pól
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Dodanie 'email' do listy pól
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control-material', 'id':'user', 'placeholder': ' ', 'autocomplete': 'off'}),
            
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("Wymagane. Podaj ważny adres email.")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Ten adres email jest już zarejestrowany.")
        return email

    


class ProductForm(forms.ModelForm):
    category = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget = forms.TextInput()

    def clean_category(self):
        category_name = self.cleaned_data['category'].strip()
        if category_name:
            # Sprawdzamy, czy kategoria istnieje w bazie danych
            category, created = Category.objects.get_or_create(name=category_name)
            return category
        else:
            return None

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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder': 'Komentarz...'})}