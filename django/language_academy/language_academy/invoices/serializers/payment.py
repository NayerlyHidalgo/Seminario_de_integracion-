# invoices/serializers/payment.py
from rest_framework import serializers
from invoices.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    enrollment_number = serializers.CharField(source='enrollment.enrollment_number', read_only=True)
    student_name = serializers.CharField(source='enrollment.student.get_full_name', read_only=True)
    method_display = serializers.CharField(source='get_method_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'enrollment', 'enrollment_number', 'student_name',
            'amount', 'method', 'method_display', 'status', 'status_display',
            'reference', 'description', 'payment_date', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data)
        
        # Actualizar el monto pagado en la inscripción si el pago es aprobado
        if payment.status == Payment.APPROVED:
            enrollment = payment.enrollment
            enrollment.paid_amount += payment.amount
            enrollment.save()
        
        return payment
    
    def update(self, instance, validated_data):
        old_status = instance.status
        old_amount = instance.amount
        
        # Actualizar el pago
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Actualizar la inscripción si cambia el estado del pago
        enrollment = instance.enrollment
        if old_status != instance.status:
            if instance.status == Payment.APPROVED and old_status != Payment.APPROVED:
                # Pago aprobado: sumar al total pagado
                enrollment.paid_amount += instance.amount
            elif old_status == Payment.APPROVED and instance.status != Payment.APPROVED:
                # Pago rechazado/pendiente: restar del total pagado
                enrollment.paid_amount -= old_amount
        elif instance.status == Payment.APPROVED and old_amount != instance.amount:
            # Cambio en el monto de un pago aprobado
            enrollment.paid_amount = enrollment.paid_amount - old_amount + instance.amount
        
        enrollment.save()
        return instance