# progress/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from progress.models import UserProgress
from progress.serializers import ProgressSerializer


class ProgressViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get overall progress summary for user"""
        progress_records = self.get_queryset()
        
        total_points = sum(p.total_points for p in progress_records)
        total_time = sum(p.total_time_spent for p in progress_records)
        total_courses = progress_records.count()
        
        return Response({
            'total_points': total_points,
            'total_time_spent_minutes': total_time,
            'total_courses_enrolled': total_courses,
            'progress_by_course': ProgressSerializer(progress_records, many=True).data
        })