# languages/admin.py
from django.contrib import admin
from languages.models import Language


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'native_name', 'difficulty_level', 'difficulty_text', 'is_active', 'created_at')
    list_filter = ('difficulty_level', 'is_active', 'created_at')
    search_fields = ('name', 'native_name', 'code')
    list_editable = ('is_active', 'difficulty_level')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'native_name', 'flag_emoji')
        }),
        ('Language Details', {
            'fields': ('difficulty_level', 'description', 'total_speakers')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def difficulty_text(self, obj):
        return obj.difficulty_text
    difficulty_text.short_description = 'Difficulty'