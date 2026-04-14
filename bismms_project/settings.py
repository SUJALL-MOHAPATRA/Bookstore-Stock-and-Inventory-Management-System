#bismms_project\settings.py

"""
Django settings for BISMMS project.
Bookstore Inventory and Stock Maintenance Management System
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# ------------------------------------------------------------------
# Load environment variables from .env file
# ------------------------------------------------------------------
load_dotenv()

# ------------------------------------------------------------------
# Base directory
# ------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------------------------------------------------
# Security
# ------------------------------------------------------------------
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key-change-in-production')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = []

# ------------------------------------------------------------------
# Installed Apps
# ------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # BISMMS apps
    'apps.accounts',
    'apps.inventory',
    'apps.stock',
    'apps.suppliers',
    'apps.alerts',
    'apps.reports',
    'apps.dashboard',
    'apps.audit',
]

# ------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------------------------------------------------
# URL Configuration
# ------------------------------------------------------------------
ROOT_URLCONF = 'bismms_project.urls'

# ------------------------------------------------------------------
# Templates
# ------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # global templates folder
        'APP_DIRS': True,                  # also looks inside each app's templates/
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

# ------------------------------------------------------------------
# WSGI
# ------------------------------------------------------------------
WSGI_APPLICATION = 'bismms_project.wsgi.application'

# ------------------------------------------------------------------
# Database — PostgreSQL (credentials from .env)
# ------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'bismms_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# ------------------------------------------------------------------
# Custom user model (we will define this in accounts app)
# ------------------------------------------------------------------
AUTH_USER_MODEL = 'accounts.CustomUser'

# ------------------------------------------------------------------
# Authentication redirects
# ------------------------------------------------------------------
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# ------------------------------------------------------------------
# Password Validation
# ------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ------------------------------------------------------------------
# Internationalization
# ------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'  # IST — change if needed
USE_I18N = True
USE_TZ = True

# ------------------------------------------------------------------
# Static files (CSS, JS, Images)
# ------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # your static/ folder at root
STATIC_ROOT = BASE_DIR / 'staticfiles'    # for production collectstatic

# ------------------------------------------------------------------
# Media files (user uploads)
# ------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ------------------------------------------------------------------
# Default primary key
# ------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ------------------------------------------------------------------
# Email Configuration — Gmail SMTP
# ------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER