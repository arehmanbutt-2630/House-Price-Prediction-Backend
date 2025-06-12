from .base import *

DEBUG = True
ALLOWED_HOSTS = []

# Use local SQLite DB
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}
