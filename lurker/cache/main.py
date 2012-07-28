

class BackendInterface(object):
    """
    A simple emulation of interfaces for various backends.
    """

    # for caching systems (i.e: memcached) that does not accep
    MAX_KEY_LENGTH = None

    def get(self, value):
        raise NotImplementedError

    def set(self, key, value, timeout=None):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    def validate_key(self, key):
        """
        validates about keys that would not be portable to the related backend.
        returns (bool)
        """
        return True
