# subscriptions/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from subscriptions.views import SubscriptionViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]