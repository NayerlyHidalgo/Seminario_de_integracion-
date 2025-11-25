# invoices/models/payment.py
from django.db import models
from .enrollment import Enrollment

class Payment(models.Model):
    CASH = 'CASH'
    CARD = 'CARD'
    TRANSFER = 'TRANSFER'
    OTHER = 'OTHER'
    
    METHOD_CHOICES = [
        (CASH, 'Efectivo'),
        (CARD, 'Tarjeta'),
        (TRANSFER, 'Transferencia'),
        (OTHER, 'Otro'),
    ]
    
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    
    STATUS_CHOICES = [
        (PENDING, 'Pendiente'),
        (APPROVED, 'Aprobado'),
        (REJECTED, 'Rechazado'),
    ]
    
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=16, choices=METHOD_CHOICES, default=CASH)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=PENDING)
    reference = models.CharField(max_length=100, blank=True, help_text="Número de referencia o transacción")
    description = models.TextField(blank=True)
    payment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-payment_date',)
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
    
    def __str__(self):
        return f'Pago ${self.amount} - {self.enrollment.enrollment_number}'