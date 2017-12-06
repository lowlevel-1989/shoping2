from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=True

INTERNAL_IPS = (
    'localhost',
    '127.0.0.1',
)

INSTALLED_APPS = [
    'django_extensions',
    'debug_toolbar',
] + INSTALLED_APPS


MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = 'static'
STATIC_URL = '/static/'

MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'
