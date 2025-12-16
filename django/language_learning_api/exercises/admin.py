from django.contrib import admin
from exercises.models import Exercise, ExerciseAttempt


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'exercise_type', 'points', 'order')
    list_filter = ('exercise_type', 'lesson__course')
    search_fields = ('title', 'question')


@admin.register(ExerciseAttempt)
class ExerciseAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'exercise', 'is_correct', 'points_earned', 'completed_at')
    list_filter = ('is_correct', 'completed_at')
    readonly_fields = ('completed_at',)