# -*- coding: utf-8 -*-

import MySQLdb

from lurker_exceptions import LurkerInvalidConfigurationObjectException
from configuration import BaseLurkerConfig
import functions

class Connection(object):

    def __init__(self, configuration):

        # Configuration class must be extended from BaseLurkerConfig
        if not issubclass(configuration, BaseLurkerConfig):
            raise LurkerInvalidConfigurationObjectException('First parameter of the Connection object must be a '\
                                                            ' subclass of BaseLurkerConfig class.')

        self.db_arguments = functions.class_to_dict(configuration)
        self.db_connection = None

        self.connect()

    def connect(self):
        self.db_connection = MySQLdb.connect(**self.db_arguments)

