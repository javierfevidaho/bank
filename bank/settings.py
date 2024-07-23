import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Load locale paths
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
    os.path.join(BASE_DIR, 'core/locale'),
]

# Set debug mode based on environment variable
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Add the production domain to ALLOWED_HOSTS
ALLOWED_HOSTS.extend([
    'uneven-idalina-cyberlotto-62107c4f.koyeb.app',
    'ltd-brandea-cyberlottobank-7684fb46.koyeb.app'
])

# Custom error view configuration
handler404 = 'core.views.error_404'

# Security settings
SECRET_KEY = os.getenv('SECRET_KEY')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core.apps.CoreConfig',
    'qr_code',
    'django_extensions',
    'django.contrib.humanize',
    'rest_framework',
    'rest_framework_simplejwt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', 'English'),
    ('es', 'Español'),
]

USE_I18N = True
USE_L10N = True
USE_TZ = True

ROOT_URLCONF = 'bank.urls'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'core/templates'),
        ],
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

WSGI_APPLICATION = 'bank.wsgi.application'

# Database configuration for production (example with PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ','

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login redirect
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'

# Security settings for production
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Stripe settings
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

# Coinbase settings
COINBASE_COMMERCE_API_KEY = os.getenv('COINBASE_COMMERCE_API_KEY')
COINBASE_COMMERCE_WEBHOOK_SHARED_SECRET = os.getenv('COINBASE_COMMERCE_WEBHOOK_SHARED_SECRET')

# Debug log database configuration
logging.basicConfig(level=logging.DEBUG)
logging.debug("Database configuration: %s", DATABASES['default'])
