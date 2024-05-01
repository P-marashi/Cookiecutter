import os
from config.env import env, BASE_DIR

env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# website domain name
DOMAIN_NAME = env("DOMAIN_NAME")


# DEBUG
DEBUG = env("SETTINGS_DEBUG")


ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])


# Application definition
LOCAL_APPS = [
    '{{cookiecutter.project_slug}}.core.apps.CoreConfig',
    '{{cookiecutter.project_slug}}.common.apps.CommonConfig',
{%- if cookiecutter.use_jwt != "n" %}
    '{{cookiecutter.project_slug}}.users.apps.UsersConfig',
    '{{cookiecutter.project_slug}}.authentication.apps.AuthenticationConfig',
{%- endif %}
]

THIRD_PARTY_APPS = [
    {%- if cookiecutter.use_celery != "n" %}
    "django_celery_results",
    "django_celery_beat",
    {%- endif %}
    {%- if cookiecutter.api_framework == "RestFramework" %}
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "corsheaders",
    {%- elif cookiecutter.api_framework == "GrapheneDjango" %}
    "graphene_django",
    {%- elif cookiecutter.api_framework == "DjangoGrpcFramework" %}
    "django_grpc_framework",
    {%- elif cookiecutter.api_framework == "BasicHTML" %}
    "django-crispy-forms",
    "crispy-bootstrap5",
    {%- endif %}
    {%- if cookiecutter.use_debug_toolbar %}
    "debug_toolbar",
    {%- endif %}
    {%- if cookiecutter.use_prometheus != "n" %}
    "django_prometheus",
    {%- endif %}
    "docs",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

MIDDLEWARE = [
    {%- if cookiecutter.use_prometheus != "n" %}
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    {%- endif %}
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    {%- if cookiecutter.use_prometheus != "n" %}
    'django_prometheus.middleware.PrometheusAfterMiddleware',    
    {%- endif %}
]

ROOT_URLCONF = 'config.urls'

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

# Wsgi application declaration
WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': env.db('DATABASE_URL', default='psql://{{cookiecutter.postgres_user}}:{{cookiecutter.postgres_password}}@127.0.0.1:5432/{{cookiecutter.project_slug}}'),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

if os.environ.get('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'github_actions',
            'USER': '{{cookiecutter.postgres_user}}',
            'PASSWORD': '{{cookiecutter.postgres_password}}',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


{%- if cookiecutter.use_jwt != "n" %}
AUTH_USER_MODEL = 'users.BaseUser'
{%- endif %}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

{%- if cookiecutter.use_persian_django != "n" %}
LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True
{%- else %}
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
{%- endif %}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Media files (Uploaded Images, Uploaded files)
MEDIA_ROOT = 'media/'
MEDIA_URL = 'media/'


# Documents Root
DOCS_ROOT = "documents/build/html/"
DOCS_ACCESS = "superuser"


{%- if cookiecutter.use_debug_toolbar != "n" %}
INTERNAL_IPS = [
    "127.0.0.1",
]
{%- endif %}


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': '{{cookiecutter.project_slug}}.api.exception_handlers.drf_default_with_modifications_exception_handler',
    # 'EXCEPTION_HANDLER': '{{cookiecutter.project_slug}}.api.exception_handlers.hacksoft_proposed_exception_handler',
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': []
}


# Redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': env("REDIS_LOCATION", default="redis://localhost:6379"),
    }
}
# Cache time to live is 15 minutes.
CACHE_TTL = 60 * 15


APP_DOMAIN = env("APP_DOMAIN", default="http://localhost:8000")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# You can remove the files from settings if you dont need them.
from config.libraries.cors import *  # noqa
from config.libraries.jwt import *  # noqa
from config.libraries.sessions import *  # noqa
{%- if cookiecutter.use_celery != "n" %}
from config.libraries.celery import *
{%- endif %}
from config.libraries.swagger import *  # noqa
{%- if cookiecutter.use_prometheus != "n" %}
from config.libraries.prometheus import *
{%- endif %}
#from config.libraries.sentry import *  # noqa
#from config.libraries.email_sending import *  # noqa
