# exercises/serializers.py
from rest_framework import serializers
from exercises.models import Exercise, ExerciseAttempt


class ExerciseSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    
    class Meta:
        model = Exercise
        exclude = ['correct_answer']  # Don't expose correct answer
        read_only_fields = ['created_at']


class ExerciseAttemptSerializer(serializers.ModelSerializer):
    exercise_title = serializers.CharField(source='exercise.title', read_only=True)
    
    class Meta:
        model = ExerciseAttempt
        fields = '__all__'
        read_only_fields = ['user', 'completed_at']