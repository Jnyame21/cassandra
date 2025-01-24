from Backend.settings import *

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
]

# Cors Config
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]

# django-silk
INSTALLED_APPS += ['silk']
MIDDLEWARE += ['silk.middleware.SilkyMiddleware']
SILKY_PYTHON_PROFILER = True  # Enables code profiling
SILKY_META = True             # Add metadata

# Media config
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

