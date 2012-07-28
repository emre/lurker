# -*- coding: utf-8 -*-

import MySQLdb
import _mysql_exceptions

from lurker_exceptions import *
from configuration import BaseLurkerConfig
from singleton import Singleton

import functions


class Connection(object):

    def __init__(self, configuration=None):

        self.db_connection = None

        if configuration:
            # Configuration class must be extended from BaseLurkerConfig
            if not issubclass(configuration, BaseLurkerConfig):
                raise LurkerInvalidConfigurationObjectException('First parameter of the Connection object must be a '\
                                                                ' subclass of BaseLurkerConfig class.')
            self.configuration = configuration
            self.db_arguments = functions.configuration_class_to_dict(configuration)
            self.connect()

    def quick_connect(self, user, passwd, dbname, host="localhost", port=3306):
        """
        Provides a simple way to connect database instead of dealing with Configuration objects.
        """
        configuration = BaseLurkerConfig
        self.db_arguments = functions.configuration_class_to_dict(configuration)
        self.db_arguments.update({
            'host': host,
            'user': user,
            'passwd': passwd,
            'db': dbname,
            'port': port,
        })

        self.configuration = configuration
        self.connect()

        return self

    def connect(self):
        self.db_connection = MySQLdb.connect(**self.db_arguments)

    def _get_cursor(self, server_side=False):
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

        if server_side:
            return MySQLdb.cursors.SSCursor(self.db_connection)
        return self.db_connection.cursor()

    def execute(self, query, parameters=None):
        """
        executes the query and returns the row count.
        """
        try:
            cursor = self._get_cursor()
            cursor.execute(query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    def get_results(self, query):
        """
        returns a list of rows based on given query.
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

    def iterate(self, query, parameters=None):
        """
        returns an iterator for the result set that stored in the server.
        should be used for large result set(s) that doesn't fit into RAM.
        """
        # todo
        cursor = self._get_cursor(True)
        try:
            cursor.execute(query, parameters)
            for row in cursor:
                yield row
        finally:
            cursor.close()


class SingletonConnection(Singleton, Connection):
    pass
