import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Cargar variables de entorno
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', default='oiweiofjwoj249024wrfij3-901329032')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Hosts permitidos para Render
ALLOWED_HOSTS = []

# Si estamos en Render, agregar el hostname automáticamente
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# También permitir localhost para desarrollo
ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])

# Si necesitas agregar más hosts desde variables de entorno
if os.environ.get('ALLOWED_HOSTS'):
    ALLOWED_HOSTS.extend(os.environ.get('ALLOWED_HOSTS').split(','))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # ¡IMPORTANTE agregar aquí!
    'django.contrib.staticfiles',
    'corsheaders',               
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'control_escolar_desit_api',  # Tu app principal
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise aquí
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',      
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS - Permitir solo los orígenes necesarios (más seguro)
CORS_ALLOWED_ORIGINS = [
    "https://control-escolar-webapp-final-dgvfqz05q-keisi-perezs-projects.vercel.app",
    "http://localhost:4200",
    "http://localhost:8000",
]

# O para desarrollo, puedes permitir todos (pero quita esto en producción):
# CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True

# Métodos permitidos
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

ROOT_URLCONF = 'control_escolar_desit_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'control_escolar_desit_api.wsgi.application'

# CONFIGURACIÓN DE BASE DE DATOS PARA RENDER + NEON
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Producción (Render + Neon PostgreSQL)
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    # Desarrollo local (SQLite)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# STATIC FILES CONFIGURATION
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files (si usas)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'control_escolar_desit_api.models.BearerTokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SSL/HTTPS settings (para producción)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True