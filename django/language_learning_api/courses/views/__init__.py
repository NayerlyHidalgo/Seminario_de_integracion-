# courses/views/__init__.py
from .course import CourseViewSet
from .enrollment import EnrollmentViewSet

__all__ = ['CourseViewSet', 'EnrollmentViewSet']