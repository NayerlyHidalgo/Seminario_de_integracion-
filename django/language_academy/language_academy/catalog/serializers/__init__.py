# catalog/serializers/__init__.py
from .language import LanguageSerializer
from .course import CourseSerializer, CourseDetailSerializer

__all__ = ['LanguageSerializer', 'CourseSerializer', 'CourseDetailSerializer']