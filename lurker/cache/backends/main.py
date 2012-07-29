import hashlib
import re


class BaseBackend(object):
    """
    base cache class for various backends.
    """

    def get(self, key):
        raise NotImplementedError

    def set(self, key, value, timeout=None):
        raise NotImplementedError

    def build_query_key(self, query, parameters=None):
        if parameters:
            query = query % parameters
        m = hashlib.md5()
        m.update(query)
        return m.hexdigest()
