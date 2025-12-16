# users/views/__init__.py
from .auth import RegisterView, LoginView, LogoutView
from .profile import ProfileView

__all__ = ['RegisterView', 'LoginView', 'LogoutView', 'ProfileView']