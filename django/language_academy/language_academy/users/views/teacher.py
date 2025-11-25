# users/views/teacher.py
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from users.models import Teacher
from users.serializers import TeacherSerializer, TeacherDetailSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.select_related('user').prefetch_related('languages').all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['languages', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'languages__name']
    ordering_fields = ['experience_years', 'hourly_rate', 'user__first_name']
    ordering = ['user__first_name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeacherDetailSerializer
        return TeacherSerializer
    
    @action(detail=False, methods=['get'])
    def by_language(self, request):
        """Profesores agrupados por idioma"""
        language_param = request.query_params.get('language_id')
        if language_param:
            teachers = self.get_queryset().filter(languages__id=language_param)
        else:
            teachers = self.get_queryset()
        
        serializer = self.get_serializer(teachers, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Profesores disponibles"""
        available_teachers = self.get_queryset().filter(is_available=True)
        serializer = self.get_serializer(available_teachers, many=True)
        return Response(serializer.data)