from main import BaseBackend

import redis
import re

try:
    import json
except ImportError:
    import simplejson as json


class RedisBackend(BaseBackend):

    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_connection = redis.StrictRedis(host=host, port=port, db=db)

    def get(self, key):
        value = self.redis_connection.get(key)
        if value:
            return json.loads(self.redis_connection.get(key))
        return value

    def set(self, key, value, timeout=None):
        return self.redis_connection.setex(key, timeout, json.dumps(value))

    def delete(self, key):
        return self.redis_connection.delete(key)
