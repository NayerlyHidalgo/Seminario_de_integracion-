# progress/serializers.py
from rest_framework import serializers
from progress.models import UserProgress


class ProgressSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_language = serializers.CharField(source='course.language.name', read_only=True)
    
    class Meta:
        model = UserProgress
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'last_activity']