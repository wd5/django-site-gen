from redis import Redis, ConnectionPool
import pickle


def make_pool(app):
    return ConnectionPool(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=app.config['REDIS_DATABASE'],
        max_connections=app.config.get('REDIS_POOL_SIZE'),
    )

class Cache(object):
    def __init__(self, pool, name='cache', default_timeout=None):
        self.client = Redis(connection_pool=pool)
        self.name = name
        self.default_timeout = default_timeout
    
    def make_key(self, s):
        return ':'.join((self.name, s))
    
    def get(self, key, default=None):
        key = self.make_key(key)
        value = self.client.get(key)
        if value is None:
            return default
        return pickle.loads(value)

    def set(self, key, value, timeout=None):
        key = self.make_key(key)
        if timeout is None:
            timeout = self.default_timeout
        
        pickled_value = pickle.dumps(value)
        if timeout:
            return self.client.setex(key, pickled_value, int(timeout))
        else:
            return self.client.set(key, pickled_value)

    def delete(self, key):
        self.client.delete(self.make_key(key))
    
    def incr(self, key, delta=1):
        return self.client.incr(self.make_key(key), delta)
