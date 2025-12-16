# subscriptions/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from subscriptions.models import Subscription, Payment


class SubscriptionTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student', password='test123')

    def test_subscription_creation(self):
        subscription = Subscription.objects.create(
            user=self.user,
            subscription_type='monthly',
            expires_at=timezone.now() + timedelta(days=30)
        )
        self.assertTrue(subscription.is_active)
        self.assertEqual(str(subscription), f"{self.user.username} - monthly Subscription")

    def test_payment_creation(self):
        subscription = Subscription.objects.create(
            user=self.user,
            subscription_type='monthly',
            expires_at=timezone.now() + timedelta(days=30)
        )
        payment = Payment.objects.create(
            subscription=subscription,
            amount=29.99,
            status='completed'
        )
        self.assertEqual(payment.amount, 29.99)
        self.assertEqual(payment.status, 'completed')