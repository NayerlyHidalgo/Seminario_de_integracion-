# invoices/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from invoices.views import EnrollmentViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'payments', PaymentViewSet)

app_name = 'invoices'

urlpatterns = [
    path('', include(router.urls)),
]