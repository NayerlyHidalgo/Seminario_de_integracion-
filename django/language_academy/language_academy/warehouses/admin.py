# warehouses/admin.py
from django.contrib import admin
from warehouses.models import LearningCenter

@admin.register(LearningCenter)
class LearningCenterAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'city', 'capacity', 'classrooms', 'is_active', 'created_at']
    list_filter = ['city', 'is_active', 'created_at']
    search_fields = ['code', 'name', 'city', 'address']
