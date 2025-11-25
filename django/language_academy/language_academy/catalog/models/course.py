# catalog/models/course.py
from django.db import models
from .language import Language

class Course(models.Model):
    BEGINNER = 'BEGINNER'
    INTERMEDIATE = 'INTERMEDIATE'
    ADVANCED = 'ADVANCED'
    
    LEVEL_CHOICES = [
        (BEGINNER, 'Principiante'),
        (INTERMEDIATE, 'Intermedio'),
        (ADVANCED, 'Avanzado'),
    ]
    
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    description = models.TextField()
    level = models.CharField(max_length=16, choices=LEVEL_CHOICES, default=BEGINNER)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_weeks = models.PositiveIntegerField(help_text="Duración del curso en semanas")
    max_students = models.PositiveIntegerField(default=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("language", "level", "name")
        ordering = ("-created_at",)
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

    def __str__(self):
        return f"{self.language.name} - {self.get_level_display()}: {self.name}"