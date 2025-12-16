# languages/models/language.py
from django.db import models


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)  # ISO 639-1 code
    native_name = models.CharField(max_length=100)
    flag_emoji = models.CharField(max_length=10, blank=True)
    difficulty_level = models.PositiveIntegerField(default=1, help_text="1=Easy, 5=Very Hard")
    description = models.TextField(blank=True)
    total_speakers = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def difficulty_text(self):
        levels = {
            1: 'Very Easy',
            2: 'Easy', 
            3: 'Medium',
            4: 'Hard',
            5: 'Very Hard'
        }
        return levels.get(self.difficulty_level, 'Unknown')