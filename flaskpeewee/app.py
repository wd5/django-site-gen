import functools
import hashlib
import pickle

from flask import Flask

from flask_peewee.db import Database
from huey.queue import Invoker

from cache import Cache, make_pool
from config import Configuration, QueueConfiguration


app = Flask(__name__)
app.config.from_object(Configuration)

db = Database(app)

# connection pool and cache
redis_pool = make_pool(app)
cache = Cache(redis_pool, app.config['CACHE_NAME'])

# task queue invoker
invoker = Invoker(QueueConfiguration.QUEUE, QueueConfiguration.RESULT_STORE)

# misc app specific functionality
def cached(key_fn=lambda a, k: hashlib.md5(pickle.dumps((a, k))).hexdigest(), timeout=3600):
    def decorator(fn):
        def bust(*args, **kwargs):
            return cache.delete(key_fn(args, kwargs)) 
        def inner(*args, **kwargs):
            key = key_fn(args, kwargs)
            res = cache.get(key)
            if res is None:
                res = fn(*args, **kwargs)
                cache.set(key, res, timeout)
            return res
        inner.bust = bust
        return inner
    return decorator
