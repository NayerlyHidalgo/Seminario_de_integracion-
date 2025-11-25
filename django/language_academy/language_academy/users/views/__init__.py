# users/views/__init__.py
from .profile import UserViewSet, UserProfileViewSet
from .teacher import TeacherViewSet

__all__ = ['UserViewSet', 'UserProfileViewSet', 'TeacherViewSet']