# progress/models.py
from django.db import models
from django.contrib.auth.models import User
from courses.models import Course


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_records')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progress_records')
    total_points = models.PositiveIntegerField(default=0)
    total_time_spent = models.PositiveIntegerField(default=0)  # in minutes
    lessons_completed = models.PositiveIntegerField(default=0)
    exercises_completed = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'course']

    def __str__(self):
        return f"{self.user.username} - {self.course.title} Progress"