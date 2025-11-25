# invoices/models/enrollment.py
from django.db import models
from django.contrib.auth.models import User
from catalog.models import Course
from warehouses.models import LearningCenter

class Enrollment(models.Model):
    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    
    STATUS_CHOICES = [
        (PENDING, 'Pendiente'),
        (CONFIRMED, 'Confirmada'),
        (COMPLETED, 'Completada'),
        (CANCELLED, 'Cancelada'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_number = models.CharField(max_length=32, unique=True, blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=PENDING)
    
    # Información académica
    start_date = models.DateField()
    end_date = models.DateField()
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Información financiera
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"

    def __str__(self):
        return f'Inscripción #{self.enrollment_number} - {self.student.get_full_name()} en {self.course.name}'
    
    @property
    def balance(self):
        return self.total_amount - self.paid_amount