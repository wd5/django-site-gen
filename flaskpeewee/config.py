import logging
import os

from huey.backends.redis_backend import RedisQueue, RedisDataStore
from huey.bin.config import BaseConfiguration


APP_ROOT = os.path.dirname(os.path.realpath(__file__))


class Configuration(object):
    DATABASE = {
        'name': '{{ project_root }}{{ site_name }}.db',
        'engine': 'peewee.SqliteDatabase',
        'threadlocals': True,
    }
    DEBUG = {% if staging %}True{% else %}False{% endif %}
    SECRET_KEY = '{{ secret_key }}'
    
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    AWS_STORAGE_BUCKET_NAME = 'media.{{ site_name }}.com'
    AWS_STORAGE_BUCKET_PREFIX = '{{ site_name }}'

    APP_ROOT = APP_ROOT
    MEDIA_ROOT = '%s/media/' % (APP_ROOT)
    
    # media settings for nginx / local
    MEDIA_URL = '/media'
    
    # media settings for s3
    #MEDIA_URL = os.path.join('http://', AWS_STORAGE_BUCKET_NAME, AWS_STORAGE_BUCKET_PREFIX)
    
    # cache settings
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DATABASE = 0
    CACHE_NAME = '{{ site_name }}'


class QueueConfiguration(BaseConfiguration):
    QUEUE = RedisQueue('{{ site_name }}')
    RESULT_STORE = RedisDataStore('{{ site_name }}_data')
    LOGFILE = '{{ logs }}huey.log'
    LOGLEVEL = logging.INFO
    PERIODIC = True
    MAX_DELAY = 60
    BACKOFF = 2
    THREADS = 1
