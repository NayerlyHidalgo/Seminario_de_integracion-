# warehouses/models/center.py
from django.db import models

class LearningCenter(models.Model):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    capacity = models.PositiveIntegerField(default=100, help_text="Capacidad máxima de estudiantes")
    classrooms = models.PositiveIntegerField(default=5, help_text="Número de aulas disponibles")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Centro de Aprendizaje"
        verbose_name_plural = "Centros de Aprendizaje"
    
    def __str__(self):
        return f'{self.code} - {self.name}'