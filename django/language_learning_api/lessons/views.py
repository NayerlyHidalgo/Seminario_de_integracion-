# lessons/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from lessons.models import Lesson
from lessons.serializers import LessonSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Lesson.objects.select_related('course')
        course_id = self.request.query_params.get('course')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset.filter(is_published=True)

    @action(detail=False, methods=['get'])
    def by_course(self, request):
        course_id = request.query_params.get('course_id')
        if course_id:
            lessons = self.get_queryset().filter(course_id=course_id)
            serializer = self.get_serializer(lessons, many=True)
            return Response(serializer.data)
        return Response({'error': 'course_id required'})