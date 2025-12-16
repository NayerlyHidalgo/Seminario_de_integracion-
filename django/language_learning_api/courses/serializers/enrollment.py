# courses/serializers/enrollment.py
from rest_framework import serializers
from courses.models import Enrollment, Course


class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    course_language = serializers.CharField(source='course.language.name', read_only=True)
    course_id = serializers.IntegerField(write_only=True)
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'course_title', 'course_language', 'course_id', 'student_name', 'enrolled_at',
            'progress_percentage', 'completed_lessons', 'last_accessed',
            'is_completed', 'completed_at', 'certificate_issued'
        ]
        read_only_fields = [
            'student', 'enrolled_at', 'progress_percentage', 'completed_lessons',
            'last_accessed', 'is_completed', 'completed_at', 'certificate_issued'
        ]

    def validate_course_id(self, value):
        """Validate that the course exists and is published"""
        try:
            course = Course.objects.get(id=value)
            if not course.is_published:
                raise serializers.ValidationError("Cannot enroll in unpublished course")
            return value
        except Course.DoesNotExist:
            raise serializers.ValidationError("Course does not exist")

    def create(self, validated_data):
        """Create enrollment for current user"""
        request = self.context.get('request')
        validated_data['student'] = request.user
        
        # Check if user is already enrolled
        course_id = validated_data['course_id']
        if Enrollment.objects.filter(
            student=request.user, 
            course_id=course_id, 
            is_active=True
        ).exists():
            raise serializers.ValidationError("Already enrolled in this course")
        
        return super().create(validated_data)