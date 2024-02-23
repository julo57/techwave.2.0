from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Product, Category

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