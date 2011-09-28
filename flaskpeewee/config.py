class Configuration(object):
    DATABASE = {
        'name': '{{ site_name }}.db',
        'engine': 'peewee.SqliteDatabase',
    }
    DEBUG = {% if staging %}True{% else %}False{% endif %}
    SECRET_KEY = '{{ secret_key }}'
