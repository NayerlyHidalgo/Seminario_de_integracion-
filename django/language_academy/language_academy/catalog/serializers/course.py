# catalog/serializers/course.py
from rest_framework import serializers
from catalog.models import Course
from .language import LanguageSerializer

class CourseSerializer(serializers.ModelSerializer):
    language_name = serializers.CharField(source='language.name', read_only=True)
    language_flag = serializers.CharField(source='language.flag_icon', read_only=True)
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    enrollment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'name', 'slug', 'description', 'level', 'level_display',
            'price', 'duration_weeks', 'max_students', 'is_active',
            'language', 'language_name', 'language_flag', 'enrollment_count',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'enrollment_count']
    
    def get_enrollment_count(self, obj):
        return obj.enrollments.filter(status__in=['CONFIRMED', 'COMPLETED']).count()
    
    def create(self, validated_data):
        return Course.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class CourseDetailSerializer(CourseSerializer):
    language = LanguageSerializer(read_only=True)