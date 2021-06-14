import os

import dj_database_url

from .common import Common


class Production(Common):
    INSTALLED_APPS = Common.INSTALLED_APPS
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
    # Site
    # https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ["*"]
    INSTALLED_APPS += ("gunicorn", )

    # Q_CLUSTER = {
    #     'name': 'django_q_django',
    #     'workers': 8,
    #     'recycle': 500,
    #     'timeout': 60,
    #     'compress': True,
    #     'save_limit': 250,
    #     'queue_limit': 500,
    #     'cpu_affinity': 1,
    #     'label': 'Django Q',
    #     'redis': 'redis://redis:6379'
    # }

    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    DATABASE_URL = f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}'
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=int(os.getenv('POSTGRES_CONN_MAX_AGE', 600))
        )
    }

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.0/howto/static-files/
    # http://django-storages.readthedocs.org/en/latest/index.html
    # INSTALLED_APPS += ('storages',)
    # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # AWS_ACCESS_KEY_ID = os.getenv('DJANGO_AWS_ACCESS_KEY_ID')
    # AWS_SECRET_ACCESS_KEY = os.getenv('DJANGO_AWS_SECRET_ACCESS_KEY')
    # AWS_STORAGE_BUCKET_NAME = os.getenv('DJANGO_AWS_STORAGE_BUCKET_NAME')
    # AWS_DEFAULT_ACL = 'public-read'
    # AWS_AUTO_CREATE_BUCKET = True
    # AWS_QUERYSTRING_AUTH = False
    # MEDIA_URL = f'https://s3.amazonaws.com/{AWS_STORAGE_BUCKET_NAME}/'

    # https://developers.google.com/web/fundamentals/performance/optimizing-content-efficiency/http-caching#cache-control
    # Response can be cached by browser and any intermediary caches (i.e. it is "public") for up to 1 day
    # 86400 = (60 seconds x 60 minutes x 24 hours)
    # AWS_HEADERS = {
    #     'Cache-Control': 'max-age=86400, s-maxage=86400, must-revalidate',
    # }
