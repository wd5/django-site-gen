import logging
import os

from skew.backends.redis_backend import RedisQueue
from skew.bin.config import BaseConfiguration


APP_ROOT = os.path.dirname(os.path.realpath(__file__))


class Configuration(object):
    DATABASE = {
        'name': '{{ project_root }}{{ site_name }}.db',
        'engine': 'peewee.SqliteDatabase',
    }
    DEBUG = {% if staging %}True{% else %}False{% endif %}
    SECRET_KEY = '{{ secret_key }}'
    APP_ROOT = APP_ROOT
    MEDIA_ROOT = '%s/media/' % (APP_ROOT)
    MEDIA_URL = '/media'


class QueueConfiguration(BaseConfiguration):
    QUEUE = RedisQueue('{{ site_name }}', 'localhost:6379:0')
    LOGFILE = '{{ logs }}skew.log'
    LOGLEVEL = logging.DEBUG
