# exercises/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from exercises.views import ExerciseViewSet, ExerciseAttemptViewSet

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet)
router.register(r'exercise-attempts', ExerciseAttemptViewSet, basename='exerciseattempt')

urlpatterns = [
    path('', include(router.urls)),
]