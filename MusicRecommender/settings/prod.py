from MusicRecommender.settings.base import *

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ["DB_NAME"],
        'HOST': os.environ["DB_HOST"],
        'PORT': 5432,
        'USER': os.environ["DB_USER"],
        'PASSWORD': os.environ["DB_PASSWORD"],
    }
}
