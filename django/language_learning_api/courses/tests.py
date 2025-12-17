# courses/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from languages.models import Language
from courses.models import Course, Enrollment


class CourseModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='instructor',
            email='instructor@test.com',
            password='testpass123'
        )
        self.language = Language.objects.create(
            name='Spanish',
            code='es',
            native_name='Español'
        )
        self.course = Course.objects.create(
            title='Spanish for Beginners',
            slug='spanish-for-beginners',
            description='Learn Spanish from scratch',
            short_description='Basic Spanish course',
            language=self.language,
            instructor=self.user,
            difficulty_level='beginner',
            is_published=True
        )

    def test_course_creation(self):
        """Test course model creation"""
        self.assertEqual(self.course.title, 'Spanish for Beginners')
        self.assertEqual(self.course.enrollment_count, 0)

    def test_course_str_representation(self):
        """Test string representation"""
        expected = f"{self.course.title} - {self.language.name}"
        self.assertEqual(str(self.course), expected)


class EnrollmentModelTestCase(TestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(
            username='instructor',
            password='testpass123'
        )
        self.student = User.objects.create_user(
            username='student',
            password='testpass123'
        )
        self.language = Language.objects.create(
            name='Spanish',
            code='es',
            native_name='Español'
        )
        self.course = Course.objects.create(
            title='Spanish for Beginners',
            slug='spanish-for-beginners',
            description='Learn Spanish from scratch',
            language=self.language,
            instructor=self.instructor,
            total_lessons=10,
            is_published=True
        )

    def test_enrollment_creation(self):
        """Test enrollment model creation"""
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course
        )
        self.assertEqual(enrollment.progress_percentage, 0.0)
        self.assertEqual(enrollment.completed_lessons, 0)
        self.assertFalse(enrollment.is_completed)

    def test_enrollment_progress_update(self):
        """Test progress calculation"""
        enrollment = Enrollment.objects.create(
            student=self.student,
            course=self.course
        )
        
        # Complete some lessons
        enrollment.completed_lessons = 5
        enrollment.update_progress()
        
        self.assertEqual(enrollment.progress_percentage, 50.0)
        self.assertFalse(enrollment.is_completed)
        
        # Complete all lessons
        enrollment.completed_lessons = 10
        enrollment.update_progress()
        
        self.assertEqual(enrollment.progress_percentage, 100.0)
        self.assertTrue(enrollment.is_completed)
        self.assertIsNotNone(enrollment.completed_at)


class CourseAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.instructor = User.objects.create_user(
            username='instructor',
            password='testpass123'
        )
        self.student = User.objects.create_user(
            username='student',
            password='testpass123'
        )
        self.language = Language.objects.create(
            name='Spanish',
            code='es',
            native_name='Español'
        )
        self.course = Course.objects.create(
            title='Spanish for Beginners',
            slug='spanish-for-beginners',
            description='Learn Spanish from scratch',
            language=self.language,
            instructor=self.instructor,
            is_published=True
            estimated_duration_hours=10
        )

    def test_course_list_unauthorized(self):
        """Test course list without authentication"""
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_enrollment(self):
        """Test course enrollment"""
        self.client.force_authenticate(user=self.student)
        response = self.client.post(f'/api/courses/{self.course.id}/enroll/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check enrollment was created
        self.assertTrue(
            Enrollment.objects.filter(
                student=self.student, 
                course=self.course, 
                is_active=True
            ).exists()
        )

    def test_course_double_enrollment(self):
        """Test preventing double enrollment"""
        self.client.force_authenticate(user=self.student)
        
        # First enrollment
        response = self.client.post(f'/api/courses/{self.course.id}/enroll/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Second enrollment attempt
        response = self.client.post(f'/api/courses/{self.course.id}/enroll/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_featured_courses(self):
        """Test featured courses endpoint"""
        self.course.is_featured = True
        self.course.save()
        
        response = self.client.get('/api/courses/featured/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
