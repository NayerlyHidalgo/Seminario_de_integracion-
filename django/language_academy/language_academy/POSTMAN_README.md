# Language Academy API - Colección de Postman

## Descripción
Esta colección de Postman contiene todos los endpoints para probar la API de la Academia de Idiomas, incluyendo autenticación JWT, gestión de cursos, usuarios, inscripciones y pagos.

## Instalación y Configuración

### 1. Importar la Colección
1. Abrir Postman
2. Clic en "Import" 
3. Seleccionar el archivo `Language_Academy_API.postman_collection.json`
4. Importar también el ambiente: `Language_Academy_Environment.postman_environment.json`

### 2. Configurar el Ambiente
1. Seleccionar el ambiente "Language Academy Environment" 
2. Verificar que `base_url` esté configurado como `http://localhost:8000`
3. Las credenciales por defecto son:
   - Username: `admin`
   - Password: `admin123`

### 3. Preparar la Base de Datos
Antes de probar los endpoints, ejecutar:

```bash
cd C:\Seminario_integracion\django\language_academy
python manage.py makemigrations
python manage.py migrate
python manage.py shell < scripts\init_data.py
python manage.py runserver
```

## Uso de la Colección

### Autenticación
1. **Login**: Ejecutar el endpoint "Auth > Login" primero
   - Esto guardará automáticamente los tokens JWT en las variables de ambiente
   - Los tokens se usarán automáticamente en las siguientes peticiones

### Flujo de Prueba Recomendado

#### 1. Autenticación
- `POST /api/auth/login/` - Iniciar sesión
- `GET /api/users/users/me/` - Verificar perfil actual

#### 2. Configuración Inicial
- `GET /api/catalog/languages/` - Ver idiomas disponibles
- `GET /api/catalog/courses/` - Ver cursos disponibles
- `GET /api/warehouses/centers/` - Ver centros disponibles

#### 3. Gestión de Usuarios
- `POST /api/users/users/register/` - Registrar nuevo estudiante
- `GET /api/users/teachers/` - Ver profesores disponibles
- `GET /api/users/profiles/` - Ver perfiles de usuarios

#### 4. Inscripciones
- `POST /api/invoices/enrollments/` - Crear nueva inscripción
- `POST /api/invoices/enrollments/{id}/confirm/` - Confirmar inscripción
- `GET /api/invoices/enrollments/my_enrollments/` - Ver mis inscripciones

#### 5. Pagos
- `POST /api/invoices/payments/` - Registrar pago
- `POST /api/invoices/payments/{id}/approve/` - Aprobar pago
- `GET /api/invoices/payments/statistics/` - Ver estadísticas

## Endpoints Principales

### Autenticación
- `POST /api/auth/login/` - Iniciar sesión
- `POST /api/auth/refresh/` - Renovar token

### Catálogo
- `GET /api/catalog/languages/` - Listar idiomas
- `GET /api/catalog/courses/` - Listar cursos
- `GET /api/catalog/courses/popular/` - Cursos populares
- `GET /api/catalog/courses/by_language/` - Cursos por idioma

### Centros de Aprendizaje
- `GET /api/warehouses/centers/` - Listar centros
- `GET /api/warehouses/centers/by_city/` - Centros por ciudad
- `GET /api/warehouses/centers/{id}/statistics/` - Estadísticas del centro

### Usuarios y Profesores
- `GET /api/users/users/me/` - Mi perfil
- `POST /api/users/users/register/` - Registrar usuario
- `GET /api/users/teachers/` - Listar profesores
- `GET /api/users/teachers/available/` - Profesores disponibles

### Inscripciones
- `GET /api/invoices/enrollments/` - Listar inscripciones
- `POST /api/invoices/enrollments/` - Crear inscripción
- `GET /api/invoices/enrollments/my_enrollments/` - Mis inscripciones
- `POST /api/invoices/enrollments/{id}/confirm/` - Confirmar
- `POST /api/invoices/enrollments/{id}/cancel/` - Cancelar

### Pagos
- `GET /api/invoices/payments/` - Listar pagos
- `POST /api/invoices/payments/` - Registrar pago
- `POST /api/invoices/payments/{id}/approve/` - Aprobar
- `POST /api/invoices/payments/{id}/reject/` - Rechazar

## Filtros y Búsquedas

### Ejemplos de Filtros
```
GET /api/catalog/courses/?language=1&level=BEGINNER
GET /api/catalog/courses/?search=inglés
GET /api/invoices/enrollments/?status=CONFIRMED
GET /api/invoices/payments/?method=CARD&status=APPROVED
```

### Parámetros de Búsqueda Comunes
- `search` - Búsqueda de texto
- `language` - Filtrar por idioma
- `level` - Filtrar por nivel (BEGINNER, INTERMEDIATE, ADVANCED)
- `status` - Filtrar por estado
- `city` - Filtrar por ciudad
- `is_active` - Filtrar por activo/inactivo

## Scripts Automáticos

La colección incluye scripts que:
- Guardan automáticamente los tokens JWT al hacer login
- Refrescan tokens expirados automáticamente
- Guardan IDs de recursos creados para usar en siguientes requests
- Muestran mensajes de éxito/error en la consola

## Datos de Prueba

Después de ejecutar el script `init_data.py`, tendrás:

### Usuarios de Prueba
- **Admin**: username=`admin`, password=`admin123`
- **Profesor 1**: username=`teacher1`, password=`teacher123`
- **Profesor 2**: username=`teacher2`, password=`teacher123`
- **Estudiante 1**: username=`student1`, password=`student123`
- **Estudiante 2**: username=`student2`, password=`student123`

### Datos Disponibles
- 5 idiomas (Inglés, Español, Francés, Alemán, Italiano)
- 7 cursos de diferentes niveles
- 3 centros de aprendizaje (Bogotá, Medellín, Cartagena)
- 2 profesores configurados

## Notas Importantes

1. **Autenticación**: Siempre ejecutar login antes de otras operaciones
2. **Permisos**: Algunos endpoints requieren permisos específicos
3. **Relaciones**: Las inscripciones requieren curso, centro y estudiante válidos
4. **Estados**: Respeta los flujos de estados (PENDING → CONFIRMED → COMPLETED)
5. **Tokens**: Los tokens JWT expiran, usa el endpoint refresh si es necesario

## Troubleshooting

### Error 401 Unauthorized
- Verificar que hiciste login
- Comprobar que el token no expiró
- Usar el endpoint refresh si es necesario

### Error 404 Not Found
- Verificar que el servidor está corriendo en `http://localhost:8000`
- Comprobar que las migraciones fueron ejecutadas
- Verificar que existen los datos de prueba

### Error 400 Bad Request
- Revisar el formato del JSON en el body
- Verificar que los campos requeridos estén presentes
- Comprobar que los IDs de relaciones existen

¡Disfruta probando la API de la Academia de Idiomas! 🚀