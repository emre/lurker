# -*- coding: utf-8 -*-

import MySQLdb
import _mysql_exceptions

from lurker_exceptions import *
from configuration import BaseLurkerConfig
from singleton import Singleton

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
        """
        executes the query and returns the cursor.
        """
        cursor = self._get_cursor()
        cursor.execute(query)
        return cursor

    def get_results(self, query):
        """
        returns a list of rows based on query query.
        """
        cursor = self._get_cursor()
        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_row(self, query):
        """
        returns a single row based on given query.
        """
        cursor = self._get_cursor()
        try:
            cursor.execute(query)

            if cursor.rowcount > 1:
                raise MultipleResultsFoundException('Multiple rows returned.')

            return cursor.fetchone()
        finally:
            cursor.close()

    def debug(self):
        # todo
        pass

    def iter(self):
        """
        returns a iterator based on query. returned data will be stored in server.
        required for large result sets that doesn't fit into RAM.
        """
        # todo
        cursor = self._get_cursor()
        pass

class SingletonConnection(Singleton, Connection):
    pass