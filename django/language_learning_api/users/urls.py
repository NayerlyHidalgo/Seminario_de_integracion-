# users/urls.py
from django.urls import path
from users.views import RegisterView, LoginView, LogoutView, ProfileView

urlpatterns = [
    path('auth/register/', RegisterView, name='register'),
    path('auth/login/', LoginView, name='login'),
    path('auth/logout/', LogoutView, name='logout'),
    path('profile/', ProfileView, name='profile'),
]