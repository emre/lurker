# -*- coding: utf-8 -*-

import MySQLdb
import _mysql_exceptions
import re

from lurker_exceptions import *
from configuration import BaseLurkerConfig
from singleton import Singleton

import functions
import logging


class Connection(object):

    def __repr__(self):
        return "<Lurker Connection instance - %s>" % id(self)

    def __init__(self, configuration=None):

        self.db_connection = None

        if configuration:
            # Configuration class must be extended from BaseLurkerConfig
            if not issubclass(configuration, BaseLurkerConfig):
                # always wanted to name exceptions like that
                # deal with it
                raise LurkerInvalidConfigurationObjectException('First parameter of the Connection object must be a '\
                                                                ' subclass of BaseLurkerConfig class.')
            self.configuration = configuration
            if self.configuration.cache and self.configuration.cache_information:
                related_backend = self.configuration.cache_information.get("backend")
                self.cache = related_backend(*self.configuration.cache_information.get("args"), **self.configuration.cache_information.get("kwargs"))
            self.db_arguments = functions.configuration_class_to_dict(configuration)

            self.connect()

    def quick_connect(self, user, passwd, dbname=None, host="localhost", port=3306):
        """
        Provides a simple way to connect database instead of dealing with Configuration objects.
        """
        configuration = BaseLurkerConfig
        self.db_arguments = functions.configuration_class_to_dict(configuration)
        self.db_arguments.update({
            'host': host,
            'user': user,
            'passwd': passwd,
            'port': port,
        })

        if dbname:
            self.db_arguments.update({'db': dbname})

        self.configuration = configuration
        self.connect()

        return self

    def connect(self):
        self.db_connection = MySQLdb.connect(**self.db_arguments)

        if self.configuration.autocommit:
            self.db_connection.autocommit(True)

        if self.configuration.supress_warnings:
            from warnings import filterwarnings
            filterwarnings('ignore', category = MySQLdb.Warning)


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

    def execute(self, query, parameters=None, execute_many = False):
        """
        executes the query and returns the row count.
        """
        cursor = self._get_cursor()
        try:
            if execute_many:
                cursor.executemany(query, parameters)
            else:
                cursor.execute(query, parameters)
                
            if self.db_arguments.has_key("auto_commit") and self.db_arguments.get("autocommit"):
                self.db_connection.commit()
            # based on the query start statement, return rowcount or affectedrows
            match = re.search('^(insert|delete|update|drop|truncate|replace|create|alter)\s+', query, flags=re.IGNORECASE)
            if match:
                sub_match = re.search('^insert\s', query, flags=re.IGNORECASE)
                if sub_match:
                    return int(cursor.lastrowid)
                return int(cursor.rowcount)

        finally:
            cursor.close()

    def _execute(self, cursor, query, parameters=None, fetch_type='all', cache=False):
        if cache:
            key = self.cache.build_query_key(query, parameters)
            cache_result = self.cache.get(key)
            if not cache_result:
                logging.debug("cache miss: %s" % query)
                cursor.execute(query, parameters)
                if fetch_type == 'all':
                    result = cursor.fetchall()
                else:
                    if cursor.rowcount > 1:
                        raise MultipleResultsFoundException('Multiple rows returned.')
                    result = cursor.fetchone()
                # update cache
                self.cache.set(key, result, cache)
            else:
                logging.debug("cache hit: %s" % query)
                return cache_result

        cursor.execute(query, parameters)
        if fetch_type == 'all':
            result = cursor.fetchall()
        else:
            if cursor.rowcount > 1:
                raise MultipleResultsFoundException('Multiple rows returned.')
            result = cursor.fetchone()

        return result

    def get_results(self, query, parameters=None, cache=False):
        """
        returns a list of rows based on given query.
        """
        cursor = self._get_cursor()
        try:
            return self._execute(cursor, query, parameters, 'all', cache)
        finally:
            cursor.close()

    def get_row(self, query, parameters=None, cache=False):
        """
        returns a single row based on given query.
        """
        cursor = self._get_cursor()
        try:
            return self._execute(cursor, query, parameters, 'one', cache)
        finally:
            cursor.close()

    def iterate(self, query, parameters=None):
        """
        returns an iterator for the result set that stored in the server.
        should be used for large result set(s) that doesn't fit into RAM.
        """
        cursor = self._get_cursor(True)
        try:
            cursor.execute(query, parameters)
            for row in cursor:
                yield row
        finally:
            cursor.close()

    def execute_many(self, query, parameters = None):
        """
        Executes a lot. I mean executes all of it. Unstoppable. Local hero. Better than good guy Greg.
        """
        return self.execute(query, parameters, True)

        

class SingletonConnection(Singleton, Connection):
    pass
