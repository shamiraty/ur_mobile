
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-rj35$p25z$nw)6*q5hlzbbcg=w@brtd9!@5(t%ygx0tl&$^c8r'
DEBUG = True
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS = [
    'admin_menu',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'import_export',
    'rangefilter',
    'axes',
    'crispy_forms',
    'crispy_bootstrap5',
]
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'
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

WSGI_APPLICATION = 'project.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#settings za kawaida
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]
import os
MEDIA_URL="/media/"
MEDIA_ROOT=os.path.join(BASE_DIR,'media')
STATICFILES_DIRS = [BASE_DIR / 'static']
LOGIN_REDIRECT_URL='/home'
LOGIN_URL = '/administration/login/'


ATOMIC_REQUESTS = False
AXES_FAILURE_LIMIT = 3  # Number of login attempts allowed
AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP = True  # Locks out the user after failure limit is reached
AXES_COOLOFF_TIME = 24  # Lockout duration in hours (e.g., 24 hours)
#---------ends django axes--------------

#SESSION MAELEZO YAPO KWENYE INSTALLED APPS
#hii ni kwa ajili ya session expire kwamba account moja kutumika kwenye browser mbili
#au pc mbili,  ukilogin sehemu moja, sehemu nyingine inajitoa
#SESSION_SAVE_EVERY_REQUEST = True  # Refresh session on each request
#SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#CSRF_COOKIE_SECURE = True
#CSRF_COOKIE_HTTPONLY = True



AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',  # Use AxesBackend for Django Axes version < 5.0
     'axes.backends.AxesStandaloneBackend',  # Use AxesStandaloneBackend for Django Axes version >= 5.0
    'django.contrib.auth.backends.ModelBackend',  # Default Django authentication backend
]