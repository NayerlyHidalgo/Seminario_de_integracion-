# invoices/serializers/enrollment.py
from rest_framework import serializers
from invoices.models import Enrollment
from catalog.serializers import CourseSerializer
from warehouses.serializers import LearningCenterSerializer

class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)
    center_name = serializers.CharField(source='center.name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'student_name', 'course', 'course_name',
            'center', 'center_name', 'enrollment_number', 'status',
            'status_display', 'start_date', 'end_date', 'grade',
            'total_amount', 'paid_amount', 'discount', 'balance',
            'created_at'
        ]
        read_only_fields = ['id', 'enrollment_number', 'balance', 'created_at']
    
    def create(self, validated_data):
        # Generar número de inscripción automáticamente
        count = Enrollment.objects.count() + 1
        validated_data['enrollment_number'] = f'ENR-{count:06d}'
        return Enrollment.objects.create(**validated_data)

class EnrollmentDetailSerializer(EnrollmentSerializer):
    course = CourseSerializer(read_only=True)
    center = LearningCenterSerializer(read_only=True)
    payments = serializers.SerializerMethodField()
    
    def get_payments(self, obj):
        from .payment import PaymentSerializer
        return PaymentSerializer(obj.payments.all(), many=True).data