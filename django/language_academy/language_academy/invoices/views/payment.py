# invoices/views/payment.py
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from invoices.models import Payment
from invoices.serializers import PaymentSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('enrollment', 'enrollment__student').all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'method', 'enrollment']
    search_fields = ['reference', 'enrollment__enrollment_number', 'enrollment__student__first_name']
    ordering_fields = ['payment_date', 'amount', 'created_at']
    ordering = ['-payment_date']
    
    def get_queryset(self):
        # Estudiantes solo ven sus propios pagos
        if not self.request.user.is_staff:
            return self.queryset.filter(enrollment__student=self.request.user)
        return self.queryset
    
    @action(detail=False, methods=['get'])
    def my_payments(self, request):
        """Pagos del usuario actual"""
        payments = self.get_queryset().filter(enrollment__student=request.user)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Estadísticas de pagos"""
        queryset = self.get_queryset()
        
        stats = {
            'total_payments': queryset.count(),
            'by_status': {},
            'by_method': {},
            'total_amount': queryset.filter(status=Payment.APPROVED).aggregate(total=Sum('amount'))['total'] or 0,
        }
        
        # Estadísticas por estado
        for status_choice in Payment.STATUS_CHOICES:
            status_code = status_choice[0]
            count = queryset.filter(status=status_code).count()
            stats['by_status'][status_code] = count
        
        # Estadísticas por método
        for method_choice in Payment.METHOD_CHOICES:
            method_code = method_choice[0]
            count = queryset.filter(method=method_code).count()
            stats['by_method'][method_code] = count
        
        return Response(stats)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Aprobar pago"""
        payment = self.get_object()
        if payment.status == Payment.PENDING:
            payment.status = Payment.APPROVED
            payment.save()
            
            # Actualizar monto pagado en la inscripción
            enrollment = payment.enrollment
            enrollment.paid_amount += payment.amount
            enrollment.save()
            
            return Response({'message': 'Pago aprobado'})
        return Response({'error': 'El pago no puede ser aprobado'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Rechazar pago"""
        payment = self.get_object()
        if payment.status == Payment.PENDING:
            payment.status = Payment.REJECTED
            payment.save()
            return Response({'message': 'Pago rechazado'})
        return Response({'error': 'El pago no puede ser rechazado'}, 
                       status=status.HTTP_400_BAD_REQUEST)