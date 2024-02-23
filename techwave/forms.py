from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import FakePayment

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
        fields = ['amount', 'description', 'name', 'last_name', 'email', 'phone']