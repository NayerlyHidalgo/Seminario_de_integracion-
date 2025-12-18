# lessons/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from languages.models import Language
from courses.models import Course
from lessons.models import Lesson


class LessonModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='instructor', password='test123')
        self.language = Language.objects.create(name='Spanish', code='es', native_name='Español')
        self.course = Course.objects.create(
            title='Spanish Basics',
            slug='spanish-basics',
            description='Learn Spanish basics',
            language=self.language,
            instructor=self.user,
            estimated_duration_hours=10  # 🟢 FIX: Added required field
        )
    
    def test_lesson_creation(self):
        lesson = Lesson.objects.create(
            course=self.course,
            title='Introduction to Spanish',
            slug='intro-spanish',
            order=1,
            lesson_type='video'
        )
        self.assertEqual(str(lesson), f"{self.course.title} - {lesson.title}")
        self.assertEqual(lesson.order, 1)