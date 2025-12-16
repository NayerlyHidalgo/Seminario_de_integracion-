#!/usr/bin/env python
"""
Initialization script for Language Learning API
Creates sample data for development and testing
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'language_learning_api.settings')
django.setup()

from django.contrib.auth.models import User
from languages.models import Language
from courses.models import Course, Enrollment
from lessons.models import Lesson
from exercises.models import Exercise


def create_languages():
    """Create sample languages"""
    languages_data = [
        {'name': 'Spanish', 'code': 'es', 'native_name': 'Español', 'flag_emoji': '🇪🇸', 'difficulty_level': 2, 'total_speakers': 500000000},
        {'name': 'French', 'code': 'fr', 'native_name': 'Français', 'flag_emoji': '🇫🇷', 'difficulty_level': 2, 'total_speakers': 280000000},
        {'name': 'German', 'code': 'de', 'native_name': 'Deutsch', 'flag_emoji': '🇩🇪', 'difficulty_level': 3, 'total_speakers': 130000000},
        {'name': 'Italian', 'code': 'it', 'native_name': 'Italiano', 'flag_emoji': '🇮🇹', 'difficulty_level': 2, 'total_speakers': 65000000},
        {'name': 'Portuguese', 'code': 'pt', 'native_name': 'Português', 'flag_emoji': '🇵🇹', 'difficulty_level': 2, 'total_speakers': 260000000},
        {'name': 'Japanese', 'code': 'ja', 'native_name': '日本語', 'flag_emoji': '🇯🇵', 'difficulty_level': 5, 'total_speakers': 125000000},
        {'name': 'Mandarin', 'code': 'zh', 'native_name': '中文', 'flag_emoji': '🇨🇳', 'difficulty_level': 5, 'total_speakers': 1000000000},
        {'name': 'Korean', 'code': 'ko', 'native_name': '한국어', 'flag_emoji': '🇰🇷', 'difficulty_level': 4, 'total_speakers': 77000000},
        {'name': 'Arabic', 'code': 'ar', 'native_name': 'العربية', 'flag_emoji': '🇸🇦', 'difficulty_level': 5, 'total_speakers': 400000000},
        {'name': 'Russian', 'code': 'ru', 'native_name': 'Русский', 'flag_emoji': '🇷🇺', 'difficulty_level': 4, 'total_speakers': 260000000},
    ]
    
    for lang_data in languages_data:
        language, created = Language.objects.get_or_create(
            code=lang_data['code'],
            defaults=lang_data
        )
        if created:
            print(f"Created language: {language.name}")


def create_users():
    """Create sample users"""
    # Create superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Created superuser: admin")
    
    # Create instructors
    instructors_data = [
        {'username': 'maria_garcia', 'email': 'maria@example.com', 'first_name': 'Maria', 'last_name': 'Garcia'},
        {'username': 'jean_dubois', 'email': 'jean@example.com', 'first_name': 'Jean', 'last_name': 'Dubois'},
        {'username': 'hans_mueller', 'email': 'hans@example.com', 'first_name': 'Hans', 'last_name': 'Mueller'},
    ]
    
    for instructor_data in instructors_data:
        user, created = User.objects.get_or_create(
            username=instructor_data['username'],
            defaults={
                **instructor_data,
                'password': 'instructor123'
            }
        )
        if created:
            user.set_password('instructor123')
            user.save()
            print(f"Created instructor: {user.username}")
    
    # Create students
    students_data = [
        {'username': 'student1', 'email': 'student1@example.com', 'first_name': 'John', 'last_name': 'Doe'},
        {'username': 'student2', 'email': 'student2@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
        {'username': 'student3', 'email': 'student3@example.com', 'first_name': 'Bob', 'last_name': 'Johnson'},
    ]
    
    for student_data in students_data:
        user, created = User.objects.get_or_create(
            username=student_data['username'],
            defaults={
                **student_data,
                'password': 'student123'
            }
        )
        if created:
            user.set_password('student123')
            user.save()
            print(f"Created student: {user.username}")


def create_courses():
    """Create sample courses"""
    spanish = Language.objects.get(code='es')
    french = Language.objects.get(code='fr')
    german = Language.objects.get(code='de')
    
    maria = User.objects.get(username='maria_garcia')
    jean = User.objects.get(username='jean_dubois')
    hans = User.objects.get(username='hans_mueller')
    
    courses_data = [
        {
            'title': 'Spanish for Absolute Beginners',
            'slug': 'spanish-absolute-beginners',
            'description': 'Learn Spanish from scratch with this comprehensive beginner course.',
            'short_description': 'Start your Spanish journey here!',
            'language': spanish,
            'instructor': maria,
            'difficulty_level': 'beginner',
            'estimated_duration_hours': 40,
            'is_published': True,
            'is_featured': True,
            'what_you_will_learn': [
                'Basic Spanish vocabulary',
                'Essential grammar rules',
                'Common phrases and expressions',
                'Pronunciation fundamentals'
            ],
            'prerequisites': ['No prior Spanish knowledge required']
        },
        {
            'title': 'French Fundamentals',
            'slug': 'french-fundamentals',
            'description': 'Master the basics of French language with native speakers.',
            'short_description': 'Essential French for beginners',
            'language': french,
            'instructor': jean,
            'difficulty_level': 'beginner',
            'estimated_duration_hours': 35,
            'is_published': True,
            'what_you_will_learn': [
                'French alphabet and pronunciation',
                'Basic vocabulary',
                'Simple sentence structures',
                'Cultural insights'
            ],
            'prerequisites': []
        },
        {
            'title': 'German Grammar Intensive',
            'slug': 'german-grammar-intensive',
            'description': 'Deep dive into German grammar for intermediate learners.',
            'short_description': 'Master German grammar rules',
            'language': german,
            'instructor': hans,
            'difficulty_level': 'intermediate',
            'estimated_duration_hours': 50,
            'is_published': True,
            'what_you_will_learn': [
                'Complex German grammar',
                'Case system mastery',
                'Verb conjugations',
                'Advanced sentence structures'
            ],
            'prerequisites': ['Basic German knowledge', 'A1-A2 level proficiency']
        }
    ]
    
    for course_data in courses_data:
        course, created = Course.objects.get_or_create(
            slug=course_data['slug'],
            defaults=course_data
        )
        if created:
            print(f"Created course: {course.title}")


def create_lessons():
    """Create sample lessons"""
    spanish_course = Course.objects.get(slug='spanish-absolute-beginners')
    
    lessons_data = [
        {
            'course': spanish_course,
            'title': 'Introduction to Spanish',
            'slug': 'introduction-spanish',
            'description': 'Welcome to Spanish! Learn about the language and its importance.',
            'lesson_type': 'video',
            'order': 1,
            'content': 'Welcome to our Spanish course! In this lesson, we will introduce you to the beautiful Spanish language.',
            'estimated_duration_minutes': 15,
            'is_published': True
        },
        {
            'course': spanish_course,
            'title': 'Spanish Alphabet',
            'slug': 'spanish-alphabet',
            'description': 'Learn the Spanish alphabet and pronunciation.',
            'lesson_type': 'interactive',
            'order': 2,
            'content': 'The Spanish alphabet has 27 letters. Let\'s learn each one!',
            'estimated_duration_minutes': 20,
            'is_published': True
        },
        {
            'course': spanish_course,
            'title': 'Basic Greetings',
            'slug': 'basic-greetings',
            'description': 'Essential Spanish greetings and polite expressions.',
            'lesson_type': 'text',
            'order': 3,
            'content': 'Learn how to greet people in Spanish: Hola, Buenos días, Buenas tardes, Buenas noches.',
            'estimated_duration_minutes': 25,
            'is_published': True
        }
    ]
    
    for lesson_data in lessons_data:
        lesson, created = Lesson.objects.get_or_create(
            slug=lesson_data['slug'],
            course=lesson_data['course'],
            defaults=lesson_data
        )
        if created:
            print(f"Created lesson: {lesson.title}")


def create_exercises():
    """Create sample exercises"""
    greetings_lesson = Lesson.objects.filter(slug='basic-greetings').first()
    
    if greetings_lesson:
        exercises_data = [
            {
                'lesson': greetings_lesson,
                'title': 'Greeting Quiz',
                'exercise_type': 'multiple_choice',
                'question': 'How do you say "Good morning" in Spanish?',
                'options': ['Buenos días', 'Buenas tardes', 'Buenas noches', 'Hola'],
                'correct_answer': 'Buenos días',
                'explanation': 'Buenos días means "Good morning" in Spanish.',
                'points': 10,
                'order': 1
            },
            {
                'lesson': greetings_lesson,
                'title': 'Fill in the Blank',
                'exercise_type': 'fill_blank',
                'question': 'Complete the greeting: "___ días"',
                'correct_answer': 'Buenos',
                'explanation': 'Buenos días is the complete phrase for "Good morning".',
                'points': 15,
                'order': 2
            }
        ]
        
        for exercise_data in exercises_data:
            exercise, created = Exercise.objects.get_or_create(
                lesson=exercise_data['lesson'],
                title=exercise_data['title'],
                defaults=exercise_data
            )
            if created:
                print(f"Created exercise: {exercise.title}")


def main():
    """Run all initialization functions"""
    print("Initializing Language Learning API with sample data...")
    
    create_languages()
    create_users()
    create_courses()
    create_lessons()
    create_exercises()
    
    print("\nSample data creation completed!")
    print("\nDefault login credentials:")
    print("Superuser - Username: admin, Password: admin123")
    print("Instructor - Username: maria_garcia, Password: instructor123")
    print("Student - Username: student1, Password: student123")


if __name__ == '__main__':
    main()