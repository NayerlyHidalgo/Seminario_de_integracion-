# courses/views/enrollment.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from courses.models import Enrollment
from courses.serializers import EnrollmentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing enrollments"""
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return enrollments for current user"""
        if self.request.user.is_staff:
            return Enrollment.objects.select_related('student', 'course').all()
        return Enrollment.objects.select_related('course').filter(
            student=self.request.user, 
            is_active=True
        )

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active enrollments for current user"""
        enrollments = self.get_queryset().filter(
            is_active=True,
            is_completed=False
        ).order_by('-last_accessed')
        
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Get completed enrollments for current user"""
        enrollments = self.get_queryset().filter(
            is_completed=True
        ).order_by('-completed_at')
        
        serializer = self.get_serializer(enrollments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_lesson_complete(self, request, pk=None):
        """Mark a lesson as completed and update progress"""
        enrollment = self.get_object()
        
        # Update the enrollment progress
        enrollment.complete_lesson()
        
        return Response({
            'detail': 'Lesson marked as completed',
            'progress_percentage': enrollment.progress_percentage,
            'completed_lessons': enrollment.completed_lessons,
            'is_completed': enrollment.is_completed
        })

    @action(detail=True, methods=['get'])
    def progress(self, request, pk=None):
        """Get detailed progress information"""
        enrollment = self.get_object()
        
        return Response({
            'course': enrollment.course.title,
            'progress_percentage': enrollment.progress_percentage,
            'completed_lessons': enrollment.completed_lessons,
            'total_lessons': enrollment.course.total_lessons,
            'is_completed': enrollment.is_completed,
            'completed_at': enrollment.completed_at,
            'last_accessed': enrollment.last_accessed,
            'certificate_issued': enrollment.certificate_issued
        })