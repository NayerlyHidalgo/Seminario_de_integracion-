# courses/models/enrollment.py
from django.db import models
from django.contrib.auth.models import User
from .course import Course


class Enrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    # Progress tracking
    progress_percentage = models.FloatField(default=0.0)
    completed_lessons = models.PositiveIntegerField(default=0)
    last_accessed = models.DateTimeField(auto_now=True)
    
    # Completion tracking
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    certificate_issued = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['student', 'course']
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"

    def update_progress(self):
        """Calculate and update progress percentage"""
        if self.course.total_lessons > 0:
            self.progress_percentage = (self.completed_lessons / self.course.total_lessons) * 100
            
            # Mark as completed if all lessons are done
            if self.progress_percentage >= 100 and not self.is_completed:
                self.is_completed = True
                from django.utils import timezone
                self.completed_at = timezone.now()
        
        self.save()

    def complete_lesson(self):
        """Mark a lesson as completed and update progress"""
        self.completed_lessons += 1
        self.update_progress()