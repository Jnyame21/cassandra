from Backend.settings import *

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
]

# Cors Config
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

# Media config
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

