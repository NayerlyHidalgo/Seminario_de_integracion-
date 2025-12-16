# courses/admin.py
from django.contrib import admin
from courses.models import Course, Enrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'language', 'instructor', 'difficulty_level', 'price', 'is_free', 'is_published', 'is_featured', 'created_at')
    list_filter = ('language', 'difficulty_level', 'is_published', 'is_featured', 'is_free', 'created_at')
    search_fields = ('title', 'description', 'instructor__username', 'instructor__email')
    list_editable = ('is_published', 'is_featured', 'price')
    readonly_fields = ('slug', 'total_lessons', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'description')
        }),
        ('Course Settings', {
            'fields': ('language', 'instructor', 'difficulty_level', 'estimated_duration_hours')
        }),
        ('Media', {
            'fields': ('thumbnail',)
        }),
        ('Pricing', {
            'fields': ('price', 'is_free')
        }),
        ('Learning Content', {
            'fields': ('what_you_will_learn', 'prerequisites', 'total_lessons')
        }),
        ('Status', {
            'fields': ('is_published', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('language', 'instructor')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'progress_percentage', 'is_completed', 'is_active')
    list_filter = ('is_active', 'is_completed', 'enrolled_at', 'course__language')
    search_fields = ('student__username', 'student__email', 'course__title')
    readonly_fields = ('enrolled_at', 'last_accessed', 'completed_at')
    
    fieldsets = (
        ('Enrollment Info', {
            'fields': ('student', 'course', 'enrolled_at', 'is_active')
        }),
        ('Progress', {
            'fields': ('progress_percentage', 'completed_lessons', 'last_accessed')
        }),
        ('Completion', {
            'fields': ('is_completed', 'completed_at', 'certificate_issued')
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'course')