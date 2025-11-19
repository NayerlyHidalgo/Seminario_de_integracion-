from django.urls import path
from . import views

urlpatterns = [
    path('basics/area-tiangulo/', views.area_triangulo),
    path('basics/tabla-multiplicar/', views.tabla_multiplicar),
    path('basics/contar-mayores/', views.contar_mayores),
    path('basics/sumar-incrementos/', views.sumar_incrementos),
]