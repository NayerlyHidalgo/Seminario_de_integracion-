# warehouses/serializers/center.py
from rest_framework import serializers
from warehouses.models import LearningCenter

class LearningCenterSerializer(serializers.ModelSerializer):
    enrollment_count = serializers.SerializerMethodField()
    utilization_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = LearningCenter
        fields = [
            'id', 'code', 'name', 'address', 'city', 'phone', 'email',
            'capacity', 'classrooms', 'is_active', 'enrollment_count',
            'utilization_rate', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'enrollment_count', 'utilization_rate']
    
    def get_enrollment_count(self, obj):
        return obj.enrollments.filter(status__in=['CONFIRMED', 'COMPLETED']).count()
    
    def get_utilization_rate(self, obj):
        enrollments = self.get_enrollment_count(obj)
        return round((enrollments / obj.capacity) * 100, 2) if obj.capacity > 0 else 0