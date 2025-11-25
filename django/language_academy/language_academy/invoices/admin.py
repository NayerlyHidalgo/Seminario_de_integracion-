# invoices/admin.py
from django.contrib import admin
from invoices.models import Enrollment, Payment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['enrollment_number', 'student', 'course', 'center', 'status', 'start_date', 'total_amount', 'paid_amount', 'created_at']
    list_filter = ['status', 'course__language', 'center', 'created_at']
    search_fields = ['enrollment_number', 'student__username', 'student__first_name', 'student__last_name', 'course__name']
    raw_id_fields = ['student', 'course', 'center']
    readonly_fields = ['enrollment_number', 'balance']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['enrollment', 'amount', 'method', 'status', 'payment_date', 'created_at']
    list_filter = ['method', 'status', 'payment_date', 'created_at']
    search_fields = ['enrollment__enrollment_number', 'reference']
    raw_id_fields = ['enrollment']
