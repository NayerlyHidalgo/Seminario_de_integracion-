# lessons/admin.py
from django.contrib import admin
from lessons.models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'lesson_type', 'order', 'is_published', 'created_at')
    list_filter = ('lesson_type', 'is_published', 'course__language')
    search_fields = ('title', 'description', 'course__title')
    list_editable = ('order', 'is_published')
    prepopulated_fields = {'slug': ('title',)}