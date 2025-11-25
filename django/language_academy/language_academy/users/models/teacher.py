# users/models/teacher.py
from django.db import models
from django.contrib.auth.models import User
from catalog.models import Language

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    languages = models.ManyToManyField(Language, related_name='teachers')
    experience_years = models.PositiveIntegerField(default=0)
    education = models.TextField(blank=True, help_text="Formación académica")
    certifications = models.TextField(blank=True, help_text="Certificaciones")
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"
    
    def __str__(self):
        return f'Prof. {self.user.get_full_name() or self.user.username}'