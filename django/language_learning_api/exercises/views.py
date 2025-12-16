# exercises/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from exercises.models import Exercise, ExerciseAttempt
from exercises.serializers import ExerciseSerializer, ExerciseAttemptSerializer


class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        exercise = self.get_object()
        user_answer = request.data.get('answer', '')
        
        # Check if answer is correct
        is_correct = user_answer.strip().lower() == exercise.correct_answer.strip().lower()
        points_earned = exercise.points if is_correct else 0
        
        # Create attempt record
        attempt = ExerciseAttempt.objects.create(
            user=request.user,
            exercise=exercise,
            user_answer=user_answer,
            is_correct=is_correct,
            points_earned=points_earned
        )
        
        return Response({
            'is_correct': is_correct,
            'points_earned': points_earned,
            'explanation': exercise.explanation if not is_correct else None,
            'attempt_id': attempt.id
        })


class ExerciseAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ExerciseAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ExerciseAttempt.objects.filter(user=self.request.user)