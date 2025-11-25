"""
URL configuration for language_academy project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Authentication
    path('api/auth/', include([
        path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ])),
    
    # App URLs
    path('api/catalog/', include('catalog.urls')),
    path('api/users/', include('users.urls')),
    path('api/warehouses/', include('warehouses.urls')),
    path('api/invoices/', include('invoices.urls')),
]
