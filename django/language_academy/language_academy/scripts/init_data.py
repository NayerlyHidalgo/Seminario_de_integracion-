# scripts/init_data.py
"""
Script para poblar la base de datos con datos de ejemplo.
Ejecutar: python manage.py shell < scripts/init_data.py
"""

import os
import django
from datetime import date, timedelta
from django.contrib.auth.models import User

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'language_academy.settings')
django.setup()

from catalog.models import Language, Course
from users.models import UserProfile, Teacher
from warehouses.models import LearningCenter
from invoices.models import Enrollment, Payment

def create_sample_data():
    print("Creando datos de ejemplo...")
    
    # Crear idiomas
    languages_data = [
        {'name': 'Inglés', 'code': 'en', 'slug': 'ingles', 'flag_icon': '🇺🇸'},
        {'name': 'Español', 'code': 'es', 'slug': 'espanol', 'flag_icon': '🇪🇸'},
        {'name': 'Francés', 'code': 'fr', 'slug': 'frances', 'flag_icon': '🇫🇷'},
        {'name': 'Alemán', 'code': 'de', 'slug': 'aleman', 'flag_icon': '🇩🇪'},
        {'name': 'Italiano', 'code': 'it', 'slug': 'italiano', 'flag_icon': '🇮🇹'},
    ]
    
    languages = {}
    for lang_data in languages_data:
        language, created = Language.objects.get_or_create(
            code=lang_data['code'],
            defaults=lang_data
        )
        languages[lang_data['code']] = language
        print(f"{'Creado' if created else 'Existe'} idioma: {language.name}")
    
    # Crear centros de aprendizaje
    centers_data = [
        {
            'code': 'CTR001',
            'name': 'Centro Principal Bogotá',
            'address': 'Carrera 7 # 45-32',
            'city': 'Bogotá',
            'phone': '+57 1 234-5678',
            'email': 'bogota@academiaidiomas.com',
            'capacity': 200,
            'classrooms': 10
        },
        {
            'code': 'CTR002', 
            'name': 'Centro Norte Medellín',
            'address': 'Calle 58 # 43-21',
            'city': 'Medellín',
            'phone': '+57 4 234-5678',
            'email': 'medellin@academiaidiomas.com',
            'capacity': 150,
            'classrooms': 8
        },
        {
            'code': 'CTR003',
            'name': 'Centro Cartagena',
            'address': 'Avenida San Martín # 12-45',
            'city': 'Cartagena',
            'phone': '+57 5 234-5678',
            'email': 'cartagena@academiaidiomas.com',
            'capacity': 100,
            'classrooms': 6
        }
    ]
    
    centers = {}
    for center_data in centers_data:
        center, created = LearningCenter.objects.get_or_create(
            code=center_data['code'],
            defaults=center_data
        )
        centers[center_data['code']] = center
        print(f"{'Creado' if created else 'Existe'} centro: {center.name}")
    
    # Crear cursos
    courses_data = [
        # Inglés
        {'language': 'en', 'name': 'Inglés Básico A1', 'level': 'BEGINNER', 'price': 250000, 'duration_weeks': 12, 'slug': 'ingles-basico-a1'},
        {'language': 'en', 'name': 'Inglés Intermedio B1', 'level': 'INTERMEDIATE', 'price': 300000, 'duration_weeks': 16, 'slug': 'ingles-intermedio-b1'},
        {'language': 'en', 'name': 'Inglés Avanzado C1', 'level': 'ADVANCED', 'price': 350000, 'duration_weeks': 20, 'slug': 'ingles-avanzado-c1'},
        
        # Francés
        {'language': 'fr', 'name': 'Francés Básico A1', 'level': 'BEGINNER', 'price': 280000, 'duration_weeks': 12, 'slug': 'frances-basico-a1'},
        {'language': 'fr', 'name': 'Francés Intermedio B1', 'level': 'INTERMEDIATE', 'price': 330000, 'duration_weeks': 16, 'slug': 'frances-intermedio-b1'},
        
        # Alemán
        {'language': 'de', 'name': 'Alemán Básico A1', 'level': 'BEGINNER', 'price': 300000, 'duration_weeks': 14, 'slug': 'aleman-basico-a1'},
        {'language': 'de', 'name': 'Alemán Intermedio B1', 'level': 'INTERMEDIATE', 'price': 350000, 'duration_weeks': 18, 'slug': 'aleman-intermedio-b1'},
    ]
    
    courses = {}
    for course_data in courses_data:
        course_data['language'] = languages[course_data['language']]
        course_data['description'] = f"Curso de {course_data['name']} - Duración {course_data['duration_weeks']} semanas"
        
        course, created = Course.objects.get_or_create(
            slug=course_data['slug'],
            defaults=course_data
        )
        courses[course_data['slug']] = course
        print(f"{'Creado' if created else 'Existe'} curso: {course.name}")
    
    # Crear usuarios de ejemplo
    users_data = [
        {
            'username': 'admin',
            'email': 'admin@academiaidiomas.com',
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'password': 'admin123',
            'role': UserProfile.ADMIN,
            'is_staff': True,
            'is_superuser': True
        },
        {
            'username': 'teacher1',
            'email': 'maria.garcia@academiaidiomas.com',
            'first_name': 'María',
            'last_name': 'García',
            'password': 'teacher123',
            'role': UserProfile.TEACHER,
            'is_staff': False
        },
        {
            'username': 'teacher2',
            'email': 'john.smith@academiaidiomas.com',
            'first_name': 'John',
            'last_name': 'Smith',
            'password': 'teacher123',
            'role': UserProfile.TEACHER,
            'is_staff': False
        },
        {
            'username': 'student1',
            'email': 'carlos.lopez@email.com',
            'first_name': 'Carlos',
            'last_name': 'López',
            'password': 'student123',
            'role': UserProfile.STUDENT,
            'is_staff': False
        },
        {
            'username': 'student2',
            'email': 'ana.martinez@email.com',
            'first_name': 'Ana',
            'last_name': 'Martínez',
            'password': 'student123',
            'role': UserProfile.STUDENT,
            'is_staff': False
        }
    ]
    
    users = {}
    for user_data in users_data:
        role = user_data.pop('role')
        password = user_data.pop('password')
        
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        
        if created:
            user.set_password(password)
            user.save()
            
        users[user.username] = user
        
        # Crear perfil de usuario
        profile, profile_created = UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': role}
        )
        
        print(f"{'Creado' if created else 'Existe'} usuario: {user.username} ({profile.get_role_display()})")
    
    # Crear profesores
    teachers_data = [
        {
            'user': 'teacher1',
            'languages': ['es', 'en'],
            'experience_years': 5,
            'education': 'Licenciatura en Lenguas Modernas',
            'certifications': 'TOEFL, DELE',
            'hourly_rate': 45000
        },
        {
            'user': 'teacher2',
            'languages': ['en', 'fr'],
            'experience_years': 8,
            'education': 'Master en Lingüística Aplicada',
            'certifications': 'CELTA, DALF',
            'hourly_rate': 55000
        }
    ]
    
    for teacher_data in teachers_data:
        user = users[teacher_data['user']]
        teacher_languages = teacher_data.pop('languages')
        teacher_data['user'] = user
        
        teacher, created = Teacher.objects.get_or_create(
            user=user,
            defaults=teacher_data
        )
        
        if created:
            for lang_code in teacher_languages:
                teacher.languages.add(languages[lang_code])
        
        print(f"{'Creado' if created else 'Existe'} profesor: {teacher.user.get_full_name()}")
    
    print("Datos de ejemplo creados exitosamente!")
    return languages, centers, courses, users

if __name__ == '__main__':
    create_sample_data()