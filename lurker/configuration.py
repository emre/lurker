# -*- coding: utf-8 -*-

class BaseLurkerConfig(object):
    """
    Base Configuration object for MySQL connections.This class is not intended to be used in this form. Another
    configuration object that extends this/BaseConfig must be passed to Connection object.
    """

    # main configuration info
    host = 'localhost'
    user = 'root'
    passwd = ''
    db = ''
    port = 3306

    # mysql-python options
    use_unicode = True
    charset = 'utf8'


