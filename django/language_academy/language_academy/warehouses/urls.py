# warehouses/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from warehouses.views import LearningCenterViewSet

router = DefaultRouter()
router.register(r'centers', LearningCenterViewSet)

app_name = 'warehouses'

urlpatterns = [
    path('', include(router.urls)),
]