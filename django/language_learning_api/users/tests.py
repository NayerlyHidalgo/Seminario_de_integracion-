# users/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from users.models import UserProfile


class UserAuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post('/api/auth/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(UserProfile.objects.filter(user__username='testuser').exists())

    def test_user_login(self):
        """Test user login"""
        # Create user first
        self.client.post('/api/auth/register/', self.user_data)
        
        # Test login
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_profile_retrieval(self):
        """Test getting user profile"""
        response = self.client.get('/api/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_profile_update(self):
        """Test updating user profile"""
        update_data = {
            'native_language': 'spanish',
            'current_level': 'intermediate',
            'country': 'Spain'
        }
        response = self.client.patch('/api/profile/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Refresh profile
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.native_language, 'spanish')
        self.assertEqual(self.profile.current_level, 'intermediate')
        self.assertEqual(self.profile.country, 'Spain')