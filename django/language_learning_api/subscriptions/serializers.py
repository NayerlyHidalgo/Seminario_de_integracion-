# subscriptions/serializers.py
from rest_framework import serializers
from subscriptions.models import Subscription, Payment


class SubscriptionSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
    subscription_type = serializers.CharField(source='subscription.subscription_type', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['payment_date']