# Language Learning API

A comprehensive Django REST API for an online language learning platform. This project provides a complete backend system for managing languages, courses, lessons, exercises, and student progress tracking.

## Features

### Core Features
- **User Management**: Registration, authentication, and user profiles
- **Language Management**: Support for multiple languages with difficulty levels
- **Course Management**: Create and manage language courses with enrollments
- **Lesson System**: Structured learning content organization
- **Exercise System**: Interactive language exercises and quizzes
- **Progress Tracking**: Monitor student learning progress and achievements
- **Subscription Management**: Handle course subscriptions and payments

### Technical Features
- JWT-based authentication
- RESTful API design
- Comprehensive filtering and search
- Image upload support
- PostgreSQL database
- Django Admin interface
- Comprehensive test coverage

## Project Structure

```
language_learning_api/
├── language_learning_api/          # Main project settings
├── users/                          # User management and profiles
├── languages/                      # Language definitions
├── courses/                        # Course and enrollment management
├── lessons/                        # Lesson content management
├── exercises/                      # Exercise and quiz system
├── progress/                       # Progress tracking
├── subscriptions/                  # Subscription management
├── templates/                      # HTML templates
├── media/                          # Uploaded files
├── manage.py                       # Django management script
└── requirements.txt               # Python dependencies
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET/PUT/PATCH /api/profile/` - User profile management

### Languages
- `GET /api/languages/` - List all languages
- `GET /api/languages/{id}/` - Get language details
- `GET /api/languages/popular/` - Get popular languages
- `GET /api/languages/easy/` - Get easier languages

### Courses
- `GET /api/courses/` - List all courses
- `POST /api/courses/` - Create new course (instructors only)
- `GET /api/courses/{id}/` - Get course details
- `PUT/PATCH /api/courses/{id}/` - Update course (instructor only)
- `DELETE /api/courses/{id}/` - Delete course (instructor only)
- `POST /api/courses/{id}/enroll/` - Enroll in course
- `POST /api/courses/{id}/unenroll/` - Unenroll from course
- `GET /api/courses/featured/` - Get featured courses
- `GET /api/courses/popular/` - Get popular courses
- `GET /api/courses/my_courses/` - Get user's created courses

### Enrollments
- `GET /api/enrollments/` - List user enrollments
- `POST /api/enrollments/` - Create new enrollment
- `GET /api/enrollments/{id}/` - Get enrollment details
- `GET /api/enrollments/active/` - Get active enrollments
- `GET /api/enrollments/completed/` - Get completed enrollments
- `POST /api/enrollments/{id}/mark_lesson_complete/` - Mark lesson complete
- `GET /api/enrollments/{id}/progress/` - Get progress details

## Quick Setup

### Automated Setup (Recommended)

**For Windows:**
```bash
setup.bat
```

**For macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd language_learning_api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   DB_NAME=language_learning
   DB_USER=postgres
   DB_PASS=your-password
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. **Database Setup**
   ```bash
   # Create PostgreSQL database
   createdb language_learning
   
   # Run migrations
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load Sample Data (Optional)**
   ```bash
   python manage.py loaddata sample_languages.json
   ```

8. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

## Usage Examples

### User Registration
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student123",
    "email": "student@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "student123",
    "password": "securepass123"
  }'
```

### Get Languages
```bash
curl -X GET http://localhost:8000/api/languages/ \
  -H "Authorization: Bearer <access_token>"
```

### Enroll in Course
```bash
curl -X POST http://localhost:8000/api/courses/1/enroll/ \
  -H "Authorization: Bearer <access_token>"
```

## Testing

Run the test suite:
```bash
# Run all tests
python manage.py test

# Run tests with coverage
coverage run --source='.' manage.py test
coverage report
```

## Development

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for classes and functions
- Keep functions small and focused

### Git Workflow
1. Create feature branch from main
2. Make changes and commit
3. Push branch and create pull request
4. Code review and merge

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For questions or issues, please create an issue in the repository or contact the development team.

## Roadmap

### Upcoming Features
- Real-time chat for language exchange
- Voice recognition for pronunciation
- Gamification with badges and leaderboards
- Mobile app support
- Video lesson integration
- AI-powered personalized learning paths

### Version History
- v1.0.0 - Initial release with core features
- v1.1.0 - Added exercise system
- v1.2.0 - Progress tracking improvements
- v1.3.0 - Subscription management