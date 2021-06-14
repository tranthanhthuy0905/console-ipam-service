import os

import dj_database_url

from .common import Common


class Development(Common):
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
    #     'redis': 'redis://redis_dev:6379'
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
