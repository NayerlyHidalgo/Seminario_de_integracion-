# warehouses/views/center.py
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from warehouses.models import LearningCenter
from warehouses.serializers import LearningCenterSerializer

class LearningCenterViewSet(viewsets.ModelViewSet):
    queryset = LearningCenter.objects.all()
    serializer_class = LearningCenterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'is_active']
    search_fields = ['name', 'code', 'city', 'address']
    ordering_fields = ['name', 'capacity', 'created_at']
    ordering = ['name']
    
    @action(detail=False, methods=['get'])
    def by_city(self, request):
        """Centros agrupados por ciudad"""
        centers_by_city = {}
        for center in self.get_queryset():
            city = center.city or 'Sin ciudad'
            if city not in centers_by_city:
                centers_by_city[city] = []
            centers_by_city[city].append(LearningCenterSerializer(center).data)
        return Response(centers_by_city)
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Estadísticas del centro"""
        center = self.get_object()
        enrollments = center.enrollments.all()
        active_enrollments = enrollments.filter(status__in=['CONFIRMED']).count()
        completed_enrollments = enrollments.filter(status='COMPLETED').count()
        
        return Response({
            'center': center.name,
            'active_enrollments': active_enrollments,
            'completed_enrollments': completed_enrollments,
            'total_enrollments': enrollments.count(),
            'capacity': center.capacity,
            'utilization_rate': round((active_enrollments / center.capacity) * 100, 2) if center.capacity > 0 else 0
        })