from Backend.settings import *
from google.oauth2 import service_account

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'eduaap.onrender.com',
]

# Cors Config
CORS_ALLOWED_ORIGINS = [
    'https://eduaap.vercel.app',
]

# Media Config (Google Cloud Storage)
GS_CREDENTIALS = service_account.Credentials.from_service_account_file("gcs-service.json")

GS_MEDIA_URL = 'https://storage.googleapis.com/eduaap-bkt/media/'


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "bucket_name": "eduaap-bkt",
            "project_id": "vivid-vent-387111",
            "default_acl": 'publicRead',
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

