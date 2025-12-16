# languages/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from languages.views import LanguageViewSet

router = DefaultRouter()
router.register(r'languages', LanguageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]