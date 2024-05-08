from Backend.settings import *
from google.oauth2 import service_account
import json

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [
    'cassandra.onrender.com',
    'localhost',
]

# Cors Config
CORS_ALLOWED_ORIGINS = [
    'https://cassandra.vercel.app',
    'http://localhost:3000',
]

# Media Config (Google Cloud Storage)
credentials_info = os.environ.get('GCS_CREDENTIALS')
if credentials_info:
    credentials_dict = json.loads(credentials_info)
    GS_CREDENTIALS = service_account.Credentials.from_service_account_info(credentials_dict)
    
else:
    raise ValueError("GCS_CREDENTIALS environment variable is not set")


GS_MEDIA_URL = 'https://storage.googleapis.com/cassandra-bkt/'


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "bucket_name": "cassandra-bkt",
            "project_id": "vivid-vent-387111",
            "default_acl": 'publicRead',
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        
    },
}

