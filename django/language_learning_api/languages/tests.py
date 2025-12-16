# languages/tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from languages.models import Language


class LanguageModelTestCase(TestCase):
    def setUp(self):
        self.language = Language.objects.create(
            name='Spanish',
            code='es',
            native_name='Español',
            flag_emoji='🇪🇸',
            difficulty_level=2,
            description='Romance language spoken in Spain and Latin America',
            total_speakers=500000000
        )

    def test_language_creation(self):
        """Test language model creation"""
        self.assertEqual(self.language.name, 'Spanish')
        self.assertEqual(self.language.code, 'es')
        self.assertEqual(self.language.difficulty_text, 'Easy')

    def test_language_str_representation(self):
        """Test string representation"""
        self.assertEqual(str(self.language), 'Spanish (es)')


class LanguageAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test languages
        Language.objects.create(
            name='Spanish',
            code='es',
            native_name='Español',
            difficulty_level=2,
            total_speakers=500000000
        )
        Language.objects.create(
            name='Mandarin',
            code='zh',
            native_name='中文',
            difficulty_level=5,
            total_speakers=1000000000
        )
        Language.objects.create(
            name='French',
            code='fr',
            native_name='Français',
            difficulty_level=3,
            total_speakers=280000000
        )

    def test_language_list_unauthorized(self):
        """Test that language list is accessible without authentication"""
        response = self.client.get('/api/languages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_language_list_authorized(self):
        """Test language list with authentication"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/languages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_language_filter_by_difficulty(self):
        """Test filtering languages by difficulty"""
        response = self.client.get('/api/languages/?difficulty=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Spanish')

    def test_language_search(self):
        """Test searching languages"""
        response = self.client.get('/api/languages/?search=spanish')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_popular_languages_endpoint(self):
        """Test popular languages endpoint"""
        response = self.client.get('/api/languages/popular/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should be ordered by total speakers (Mandarin first)
        self.assertEqual(response.data[0]['name'], 'Mandarin')

    def test_easy_languages_endpoint(self):
        """Test easy languages endpoint"""
        response = self.client.get('/api/languages/easy/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only include Spanish (difficulty 2)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Spanish')