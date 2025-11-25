# users/admin.py
from django.contrib import admin
from users.models import UserProfile, Teacher

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']
    raw_id_fields = ['user']

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['user', 'experience_years', 'hourly_rate', 'is_available', 'created_at']
    list_filter = ['languages', 'is_available', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    raw_id_fields = ['user']
    filter_horizontal = ['languages']
