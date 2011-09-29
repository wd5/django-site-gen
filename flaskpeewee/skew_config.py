import logging

config = {
    'queue': 'skew.backends.redis_backend.RedisQueue',
    'name': 'skew',
    'conn': 'localhost:6379:0',
    'threads': 1,
    'logfile': '{{ logs }}skew.log',
    'loglevel': logging.DEBUG,
}
