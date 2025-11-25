# catalog/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from catalog.views import LanguageViewSet, CourseViewSet

router = DefaultRouter()
router.register(r'languages', LanguageViewSet)
router.register(r'courses', CourseViewSet)

app_name = 'catalog'

urlpatterns = [
    path('', include(router.urls)),
]