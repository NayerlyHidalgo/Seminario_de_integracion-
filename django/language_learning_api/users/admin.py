# users/admin.py
from django.contrib import admin
from users.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'native_language', 'current_level', 'streak_count', 'total_study_time', 'created_at')
    list_filter = ('native_language', 'current_level', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('total_study_time', 'streak_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Language Settings', {
            'fields': ('native_language', 'target_languages', 'current_level')
        }),
        ('Personal Information', {
            'fields': ('bio', 'avatar', 'date_of_birth', 'country', 'timezone')
        }),
        ('Learning Progress', {
            'fields': ('daily_goal_minutes', 'streak_count', 'total_study_time')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )