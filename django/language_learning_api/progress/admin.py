from django.contrib import admin
from progress.models import UserProgress


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'total_points', 'lessons_completed', 'current_streak', 'last_activity')
    list_filter = ('course__language', 'last_activity')
    search_fields = ('user__username', 'course__title')
    readonly_fields = ('created_at', 'last_activity')