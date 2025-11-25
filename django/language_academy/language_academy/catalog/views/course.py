# catalog/views/course.py
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from catalog.models import Course
from catalog.serializers import CourseSerializer, CourseDetailSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.select_related('language').all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['language', 'level', 'is_active']
    search_fields = ['name', 'description', 'language__name']
    ordering_fields = ['name', 'price', 'created_at', 'duration_weeks']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer
    
    @action(detail=False, methods=['get'])
    def by_language(self, request):
        """Listar cursos agrupados por idioma"""
        languages = {}
        for course in self.get_queryset():
            lang_name = course.language.name
            if lang_name not in languages:
                languages[lang_name] = []
            languages[lang_name].append(CourseSerializer(course).data)
        return Response(languages)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Cursos más populares (con más inscripciones)"""
        popular_courses = self.get_queryset().filter(is_active=True)[:10]
        serializer = self.get_serializer(popular_courses, many=True)
        return Response(serializer.data)