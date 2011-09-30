import os

APP_ROOT = os.path.dirname(os.path.realpath(__file__))

class Configuration(object):
    DATABASE = {
        'name': '{{ site_name }}.db',
        'engine': 'peewee.SqliteDatabase',
    }
    DEBUG = {% if staging %}True{% else %}False{% endif %}
    SECRET_KEY = '{{ secret_key }}'
