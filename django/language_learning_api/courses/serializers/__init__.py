# courses/serializers/__init__.py
from .course import CourseSerializer, CourseDetailSerializer
from .enrollment import EnrollmentSerializer

__all__ = ['CourseSerializer', 'CourseDetailSerializer', 'EnrollmentSerializer']