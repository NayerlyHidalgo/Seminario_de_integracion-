# exercises/models.py
from django.db import models
from django.contrib.auth.models import User
from lessons.models import Lesson


class Exercise(models.Model):
    EXERCISE_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('fill_blank', 'Fill in the Blank'),
        ('matching', 'Matching'),
        ('translation', 'Translation'),
        ('pronunciation', 'Pronunciation'),
        ('listening', 'Listening'),
    ]
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='exercises')
    title = models.CharField(max_length=200)
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_TYPES)
    question = models.TextField()
    options = models.JSONField(default=list, blank=True)  # For multiple choice
    correct_answer = models.TextField()
    explanation = models.TextField(blank=True)
    points = models.PositiveIntegerField(default=10)
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['lesson', 'order']

    def __str__(self):
        return f"{self.lesson.title} - {self.title}"


class ExerciseAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercise_attempts')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='attempts')
    user_answer = models.TextField()
    is_correct = models.BooleanField()
    points_earned = models.PositiveIntegerField(default=0)
    attempt_number = models.PositiveIntegerField(default=1)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.user.username} - {self.exercise.title}"