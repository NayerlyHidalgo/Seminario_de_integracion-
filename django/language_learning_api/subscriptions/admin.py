from django.contrib import admin
from subscriptions.models import Subscription, Payment


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_type', 'status', 'started_at', 'expires_at', 'auto_renewal')
    list_filter = ('subscription_type', 'status', 'auto_renewal')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('started_at', 'created_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'amount', 'currency', 'status', 'payment_date')
    list_filter = ('status', 'currency', 'payment_date')
    search_fields = ('subscription__user__username', 'transaction_id')
    readonly_fields = ('payment_date',)