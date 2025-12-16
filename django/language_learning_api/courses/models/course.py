# courses/models/course.py
from django.db import models
from django.contrib.auth.models import User
from languages.models import Language


class Course(models.Model):
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('elementary', 'Elementary'),
        ('intermediate', 'Intermediate'),
        ('upper_intermediate', 'Upper Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='courses')
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_courses')
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    
    # Course content
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    estimated_duration_hours = models.PositiveIntegerField(help_text="Estimated hours to complete")
    total_lessons = models.PositiveIntegerField(default=0)
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_free = models.BooleanField(default=True)
    
    # Course status
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Learning objectives
    what_you_will_learn = models.JSONField(default=list, blank=True)
    prerequisites = models.JSONField(default=list, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['language', 'slug']

    def __str__(self):
        return f"{self.title} - {self.language.name}"

    @property
    def enrollment_count(self):
        """Get the number of enrolled students"""
        return self.enrollments.filter(is_active=True).count()

    @property
    def average_rating(self):
        """Calculate average rating from student feedback"""
        # This would be implemented when we add a rating system
        return 0.0

    def update_lesson_count(self):
        """Update the total number of lessons in this course"""
        self.total_lessons = self.lessons.count()
        self.save()