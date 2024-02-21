from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
  
urlpatterns = [
   path('', views.home, name='home'),
   path('main', views.main, name='main'),
   # Usunięto niestandardowy widok logowania, aby uniknąć konfliktu
   path('register', views.register, name='register'),
   path('chek', views.chek, name='chek'),
   path('productsite', views.productsite, name='productsite'),
   path('profile', views.profile, name='profile'),

   # Logowanie używając wbudowanego widoku
   path('login', auth_views.LoginView.as_view(template_name='techwave/Login & Register/login.html'), name='login'),
   # Wylogowanie
   path('logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
   # Zmiana hasła
   path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
   path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
   # Reset hasła
   path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
   path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
