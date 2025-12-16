# lessons/models.py
from django.db import models
from courses.models import Course


class Lesson(models.Model):
    LESSON_TYPES = [
        ('video', 'Video'),
        ('text', 'Text'),
        ('audio', 'Audio'),
        ('interactive', 'Interactive'),
        ('quiz', 'Quiz'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220)
    description = models.TextField(blank=True)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES, default='text')
    order = models.PositiveIntegerField()
    
    # Content
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    audio_file = models.FileField(upload_to='lesson_audio/', blank=True)
    thumbnail = models.ImageField(upload_to='lesson_thumbnails/', blank=True)
    
    # Settings
    estimated_duration_minutes = models.PositiveIntegerField(default=10)
    is_required = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['course', 'order']
        unique_together = ['course', 'slug']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update course lesson count
        self.course.update_lesson_count()