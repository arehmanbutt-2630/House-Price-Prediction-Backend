from .base import *

DEBUG = False

ALLOWED_HOSTS = ['13.53.134.97', 'ec2-13-53-134-97.eu-north-1.compute.amazonaws.com']

# I can change this if I use PostgreSQL on EC2 later
DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
}
