# invoices/views/enrollment.py
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum
from invoices.models import Enrollment
from invoices.serializers import EnrollmentSerializer, EnrollmentDetailSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related('student', 'course', 'center').all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'course', 'center', 'student']
    search_fields = ['enrollment_number', 'student__first_name', 'student__last_name', 'course__name']
    ordering_fields = ['created_at', 'start_date', 'total_amount']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EnrollmentDetailSerializer
        return EnrollmentSerializer
    
    def get_queryset(self):
        # Estudiantes solo ven sus propias inscripciones
        if not self.request.user.is_staff:
            return self.queryset.filter(student=self.request.user)
        return self.queryset
    
    @action(detail=False, methods=['get'])
    def my_enrollments(self, request):
        """Inscripciones del usuario actual"""
        enrollments = self.get_queryset().filter(student=request.user)
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Estadísticas de inscripciones"""
        queryset = self.get_queryset()
        
        stats = {
            'total_enrollments': queryset.count(),
            'by_status': {},
            'total_revenue': queryset.aggregate(total=Sum('total_amount'))['total'] or 0,
            'total_paid': queryset.aggregate(total=Sum('paid_amount'))['total'] or 0,
        }
        
        # Estadísticas por estado
        for status_choice in Enrollment.STATUS_CHOICES:
            status_code = status_choice[0]
            count = queryset.filter(status=status_code).count()
            stats['by_status'][status_code] = count
        
        return Response(stats)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirmar inscripción"""
        enrollment = self.get_object()
        if enrollment.status == Enrollment.PENDING:
            enrollment.status = Enrollment.CONFIRMED
            enrollment.save()
            return Response({'message': 'Inscripción confirmada'})
        return Response({'error': 'La inscripción no puede ser confirmada'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancelar inscripción"""
        enrollment = self.get_object()
        if enrollment.status in [Enrollment.PENDING, Enrollment.CONFIRMED]:
            enrollment.status = Enrollment.CANCELLED
            enrollment.save()
            return Response({'message': 'Inscripción cancelada'})
        return Response({'error': 'La inscripción no puede ser cancelada'}, 
                       status=status.HTTP_400_BAD_REQUEST)