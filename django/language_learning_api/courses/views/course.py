# courses/views/course.py
from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from courses.models import Course, Enrollment
from courses.serializers import CourseSerializer, CourseDetailSerializer


class CoursePermission(permissions.BasePermission):
    """Custom permission for courses"""
    
    def has_permission(self, request, view):
        # Allow read access to everyone
        if view.action in ['list', 'retrieve']:
            return True
        # Only authenticated users can create/update
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Allow read access to everyone
        if view.action == 'retrieve':
            return True
        # Only instructor can modify their courses
        if view.action in ['update', 'partial_update', 'destroy']:
            return obj.instructor == request.user or request.user.is_staff
        return True


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for managing courses"""
    queryset = Course.objects.select_related('language', 'instructor').annotate(
        enrollment_count=Count('enrollments', filter=Q(enrollments__is_active=True))
    )
    permission_classes = [CoursePermission]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'short_description', 'language__name']
    ordering_fields = ['created_at', 'title', 'difficulty_level', 'price']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter courses based on query parameters"""
        queryset = super().get_queryset()
        
        # Only show published courses for non-staff users
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
        
        # Filter by language
        language = self.request.query_params.get('language')
        if language:
            queryset = queryset.filter(language__code=language)
        
        # Filter by difficulty level
        difficulty = self.request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except ValueError:
                pass
        
        max_price = self.request.query_params.get('max_price')
        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except ValueError:
                pass
        
        # Filter free courses
        is_free = self.request.query_params.get('is_free')
        if is_free and is_free.lower() in ('true', '1', 'yes'):
            queryset = queryset.filter(is_free=True)
        
        # Filter by instructor
        instructor = self.request.query_params.get('instructor')
        if instructor:
            queryset = queryset.filter(instructor__username=instructor)
        
        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured courses"""
        courses = self.get_queryset().filter(is_featured=True)[:10]
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular courses by enrollment count"""
        courses = self.get_queryset().order_by('-enrollment_count')[:10]
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_courses(self, request):
        """Get courses created by current user"""
        if not request.user.is_authenticated:
            return Response({'detail': 'Authentication required'}, 
                          status=status.HTTP_401_UNAUTHORIZED)
        
        courses = self.get_queryset().filter(instructor=request.user)
        serializer = self.get_serializer(courses, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        """Enroll current user in the course"""
        course = self.get_object()
        
        if not course.is_published:
            return Response({'detail': 'Course is not published'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Check if already enrolled
        if Enrollment.objects.filter(
            student=request.user, 
            course=course, 
            is_active=True
        ).exists():
            return Response({'detail': 'Already enrolled in this course'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Create enrollment
        enrollment = Enrollment.objects.create(
            student=request.user,
            course=course
        )
        
        return Response({
            'detail': 'Successfully enrolled in course',
            'enrollment_id': enrollment.id
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def unenroll(self, request, pk=None):
        """Unenroll current user from the course"""
        course = self.get_object()
        
        try:
            enrollment = Enrollment.objects.get(
                student=request.user, 
                course=course, 
                is_active=True
            )
            enrollment.is_active = False
            enrollment.save()
            
            return Response({'detail': 'Successfully unenrolled from course'})
        except Enrollment.DoesNotExist:
            return Response({'detail': 'Not enrolled in this course'}, 
                          status=status.HTTP_400_BAD_REQUEST)