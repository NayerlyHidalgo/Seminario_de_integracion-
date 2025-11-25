# users/serializers/teacher.py
from rest_framework import serializers
from users.models import Teacher
from catalog.serializers import LanguageSerializer

class TeacherSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    languages_taught = serializers.SerializerMethodField()
    
    class Meta:
        model = Teacher
        fields = [
            'id', 'user', 'user_name', 'user_email', 'languages',
            'languages_taught', 'experience_years', 'education',
            'certifications', 'hourly_rate', 'is_available',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_languages_taught(self, obj):
        return [lang.name for lang in obj.languages.all()]

class TeacherDetailSerializer(TeacherSerializer):
    languages = LanguageSerializer(many=True, read_only=True)