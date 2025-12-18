# progress/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from languages.models import Language
from courses.models import Course
from progress.models import UserProgress


class ProgressTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student', password='test123')
        self.instructor = User.objects.create_user(username='instructor', password='test123')
        self.language = Language.objects.create(name='Spanish', code='es', native_name='Español')
        self.course = Course.objects.create(
            title='Spanish Basics',
            slug='spanish-basics',
            description='Learn Spanish basics',
            language=self.language,
            instructor=self.instructor,
            estimated_duration_hours=10  # 🟢 FIX: Added required field
        )

    def test_progress_creation(self):
        progress = UserProgress.objects.create(
            user=self.user,
            course=self.course,
            total_points=100
        )
        self.assertEqual(str(progress), f"{self.user.username} - {self.course.title} Progress")
        self.assertEqual(progress.total_points, 100)