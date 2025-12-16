# users/models/profile.py
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    PROFICIENCY_LEVELS = [
        ('beginner', 'Beginner'),
        ('elementary', 'Elementary'),
        ('intermediate', 'Intermediate'),
        ('upper_intermediate', 'Upper Intermediate'),
        ('advanced', 'Advanced'),
        ('proficient', 'Proficient'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    native_language = models.CharField(max_length=50, default='english')
    target_languages = models.JSONField(default=list, blank=True)
    current_level = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS, default='beginner')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    daily_goal_minutes = models.PositiveIntegerField(default=15)
    streak_count = models.PositiveIntegerField(default=0)
    total_study_time = models.PositiveIntegerField(default=0)  # in minutes
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()

    def add_study_time(self, minutes):
        """Add study time and update streak if needed"""
        self.total_study_time += minutes
        self.save()