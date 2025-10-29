import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='your-secret-key-here')
DEBUG = config('DEBUG', default=True, cast=bool)

INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'channels',

    # Core Apps
    'core',
    'dashboard',

    # Smart Home IoT Apps
    'devices',
    'security',
    'energy',
    'automation',

    # AI Architecture & Design Apps
    'ai_assistant',
    'architecture',
    'design',
    'materials',
    'architects',
    'consultation',

    # User Management Apps
    'accounts',
    'profile',
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
]

ROOT_URLCONF = 'safenest.urls'
ASGI_APPLICATION = 'safenest.asgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Channels
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}

# Celery
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# OpenRouter AI API Configuration
OPENROUTER_API_KEY = config('OPENROUTER_API_KEY', default=None)

# Debug: Print API key status (remove in production)
if OPENROUTER_API_KEY:
    print(f"✅ OpenRouter API Key loaded: ***{OPENROUTER_API_KEY[-4:]}")
else:
    print("❌ OpenRouter API Key not found in environment")

# AI Assistant Settings
AI_ASSISTANT_SETTINGS = {
    'DEFAULT_MODEL': 'z-ai/glm-4.5-air:free',
    'FALLBACK_MODEL': 'anthropic/claude-3-haiku',  # Working fallback model
    'MAX_TOKENS': 500,
    'TEMPERATURE': 0.7,
    'TOP_P': 0.9,
    'TIMEOUT': 30,
    'MAX_HISTORY_MESSAGES': 10,
}