# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, UserProfileViewSet, TeacherViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'teachers', TeacherViewSet)

app_name = 'users'

urlpatterns = [
    path('', include(router.urls)),
]