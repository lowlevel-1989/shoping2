from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=False
SENDGRID_SANDBOX_MODE_IN_DEBUG = DEBUG

STATIC_ROOT = 'static'
STATIC_URL = '/static/'

MEDIA_ROOT = 'media'
MEDIA_URL = '/media/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console'],
            },
        },
    }
