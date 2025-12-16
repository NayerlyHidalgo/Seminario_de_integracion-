# languages/views/language.py
from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from languages.models import Language
from languages.serializers import LanguageSerializer


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for languages - read-only for regular users
    Admin can manage through Django admin
    """
    queryset = Language.objects.filter(is_active=True)
    serializer_class = LanguageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'native_name', 'code']
    ordering_fields = ['name', 'difficulty_level', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        """Filter languages based on query parameters"""
        queryset = super().get_queryset()
        
        # Filter by difficulty level
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            try:
                queryset = queryset.filter(difficulty_level=int(difficulty))
            except ValueError:
                pass
        
        # Filter by minimum difficulty
        min_difficulty = self.request.query_params.get('min_difficulty')
        if min_difficulty:
            try:
                queryset = queryset.filter(difficulty_level__gte=int(min_difficulty))
            except ValueError:
                pass
        
        # Filter by maximum difficulty
        max_difficulty = self.request.query_params.get('max_difficulty')
        if max_difficulty:
            try:
                queryset = queryset.filter(difficulty_level__lte=int(max_difficulty))
            except ValueError:
                pass
        
        return queryset

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get most popular languages by total speakers"""
        languages = self.get_queryset().filter(
            total_speakers__isnull=False
        ).order_by('-total_speakers')[:10]
        
        serializer = self.get_serializer(languages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def easy(self, request):
        """Get easier languages (difficulty 1-2)"""
        languages = self.get_queryset().filter(difficulty_level__lte=2)
        serializer = self.get_serializer(languages, many=True)
        return Response(serializer.data)