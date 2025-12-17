# courses/serializers/course.py
from rest_framework import serializers
from courses.models import Course
from languages.serializers import LanguageSerializer


class CourseSerializer(serializers.ModelSerializer):
    """Basic course serializer for list views"""
    language = LanguageSerializer(read_only=True)
    language_id = serializers.IntegerField(write_only=True)
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    enrollment_count = serializers.IntegerField(source='active_enrollments_count', read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'short_description', 'language', 'language_id',
            'instructor_name', 'difficulty_level', 'thumbnail', 'estimated_duration_hours',
            'total_lessons', 'price', 'is_free', 'is_featured', 'enrollment_count',
            'average_rating', 'created_at'
        ]
        read_only_fields = ['slug', 'total_lessons', 'created_at']


class CourseDetailSerializer(serializers.ModelSerializer):
    """Detailed course serializer for detail views"""
    language = LanguageSerializer(read_only=True)
    language_id = serializers.IntegerField(write_only=True)
    instructor_name = serializers.CharField(source='instructor.get_full_name', read_only=True)
    instructor_username = serializers.CharField(source='instructor.username', read_only=True)
    enrollment_count = serializers.IntegerField(source='active_enrollments_count', read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    is_enrolled = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['instructor', 'slug', 'total_lessons', 'created_at', 'updated_at']

    def get_is_enrolled(self, obj):
        """Check if current user is enrolled in this course"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.enrollments.filter(student=request.user, is_active=True).exists()
        return False

    def validate(self, attrs):
        """Validate course data"""
        if attrs.get('price', 0) > 0:
            attrs['is_free'] = False
        else:
            attrs['is_free'] = True
        return attrs

    def create(self, validated_data):
        """Create course with current user as instructor"""
        request = self.context.get('request')
        validated_data['instructor'] = request.user
        
        # Generate slug from title
        from django.utils.text import slugify
        validated_data['slug'] = slugify(validated_data['title'])
        
        return super().create(validated_data)