# -*- coding: utf-8 -*-

import sys, random, time
sys.path.append('..')

import unittest

from config import TestConfig, FakeConfig
from lurker.connection import Connection
from lurker.lurker_exceptions import LurkerInvalidConfigurationObjectException, LurkerNoConnectivityException, MultipleResultsFoundException

class TestLurker(unittest.TestCase):

    def setUp(self):
        self.connection = Connection(TestConfig)

    def test_valid_configuration_class(self):
        assert isinstance(Connection(TestConfig), Connection)

    def test_invalid_configuration_class(self):
        self.assertRaises(LurkerInvalidConfigurationObjectException, Connection, FakeConfig)

    def test_quick_connect(self):
        connection = Connection().quick_connect(TestConfig.user, TestConfig.passwd, TestConfig.db)
        assert isinstance(Connection(TestConfig), Connection)

    def test_connectivity_control(self):
        connection = Connection(TestConfig)
        connection.db_connection = None
        self.assertRaises(LurkerNoConnectivityException, connection.get_results, "SELECT * FROM people")

    def test_return_value(self):
        name = random.randint(0, 10000000)
        retval = self.connection.execute('INSERT INTO people(name) VALUES(%s)', [name, ])
        assert isinstance(retval, int)

        retval = self.connection.execute("UPDATE people SET name = 'random_is_not_random' WHERE id = %s", [retval, ])
        self.assertEqual(retval, 1)

    def test_return_value_with_none(self):
        retval = self.connection.execute("SELECT NOW()")
        assert retval == None

    def test_get_row_on_multiple_row(self):
        self.assertRaises(MultipleResultsFoundException, self.connection.get_row, "SELECT * FROM people")

    def test_cache_operations(self):
        query = "SELECT * FROM people WHERE id = 1"
        retval = self.connection.get_row(query, cache=2)

        key = self.connection.cache.build_query_key(query)
        assert self.connection.cache.get(key), None

        time.sleep(3)
        assert self.connection.cache.get(key) == None

if __name__ == '__main__':
    unittest.main()