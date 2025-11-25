# catalog/admin.py
from django.contrib import admin
from catalog.models import Language, Course

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'flag_icon', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'language', 'level', 'price', 'duration_weeks', 'is_active', 'created_at']
    list_filter = ['language', 'level', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'language__name']
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ['language']
