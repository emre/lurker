# -*- coding: utf-8 -*-

from lurker_exceptions import LurkerInvalidConfigurationObjectException
from configuration import BaseLurkerConfig

class Connection(object):

    def __init__(self, Configuration):

        # Configuration class must be extended from BaseLurkerConfig
        if not issubclass(Configuration, BaseLurkerConfig):
            raise LurkerInvalidConfigurationObjectException('First parameter of the Connection object must be a '\
                                                            ' subclass of BaseLurkerConfig class.')
