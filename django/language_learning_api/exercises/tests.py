# exercises/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from languages.models import Language
from courses.models import Course
from lessons.models import Lesson
from exercises.models import Exercise, ExerciseAttempt


class ExerciseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student', password='test123')
        self.instructor = User.objects.create_user(username='instructor', password='test123')
        self.language = Language.objects.create(name='Spanish', code='es', native_name='Español')
        self.course = Course.objects.create(
            title='Spanish Basics',
            slug='spanish-basics',
            description='Learn Spanish basics',
            language=self.language,
            instructor=self.instructor
        )
        self.lesson = Lesson.objects.create(
            course=self.course,
            title='Greetings',
            slug='greetings',
            order=1
        )
        self.exercise = Exercise.objects.create(
            lesson=self.lesson,
            title='Basic Greetings',
            exercise_type='multiple_choice',
            question='How do you say "Hello" in Spanish?',
            options=['Hola', 'Adiós', 'Gracias', 'Por favor'],
            correct_answer='Hola',
            order=1
        )

    def test_exercise_creation(self):
        self.assertEqual(str(self.exercise), f"{self.lesson.title} - {self.exercise.title}")

    def test_exercise_attempt(self):
        attempt = ExerciseAttempt.objects.create(
            user=self.user,
            exercise=self.exercise,
            user_answer='Hola',
            is_correct=True,
            points_earned=10
        )
        self.assertTrue(attempt.is_correct)
        self.assertEqual(attempt.points_earned, 10)