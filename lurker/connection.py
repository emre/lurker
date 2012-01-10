# -*- coding: utf-8 -*-

import MySQLdb
import _mysql_exceptions

from lurker_exceptions import *
from configuration import BaseLurkerConfig

import functions

class Connection(object):

    def __init__(self, configuration):

        # Configuration class must be extended from BaseLurkerConfig
        if not issubclass(configuration, BaseLurkerConfig):
            raise LurkerInvalidConfigurationObjectException('First parameter of the Connection object must be a '\
                                                            ' subclass of BaseLurkerConfig class.')
        self.configuration = configuration

        self.db_arguments = functions.configuration_class_to_dict(configuration)
        self.db_connection = None

        self.connect()

    def connect(self):
        self.db_connection = MySQLdb.connect(**self.db_arguments)

    def _get_cursor(self):
        """
        returns emulated cursor from mySQLDB library
        mostly, not intended to be used from the outside of the class.
        """
        if not self.db_connection:
            raise LurkerNoConnectivityException('Establish a database connection first')

        if self.configuration.ping_at_every_query:
            # ensures that the connection is alive.
            # can be expensive for every query for some situations. default is "off".
            # but it can be required for long-running python programs against the default
            # mysql time-out.
            try:
                self.db_connection.ping()
            except _mysql_exceptions.InterfaceError:
                self.connect()

        if not hasattr(self, 'db_cursor'):
            self.db_cursor = self.db_connection.cursor()

        return self.db_cursor

    def query(self, query):
        cursor = self._get_cursor()
        return cursor.execute(query)


