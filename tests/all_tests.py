# -*- coding: utf-8 -*-

import sys, random, time
sys.path.append('..')

import unittest

from config import TestConfig, FakeConfig
from lurker.connection import Connection
from lurker.lurker_exceptions import LurkerInvalidConfigurationObjectException, LurkerNoConnectivityException, MultipleResultsFoundException
from _mysql_exceptions import ProgrammingError


class TestLurker(unittest.TestCase):

    def setUp(self):
        self.connection = Connection(TestConfig)
        self.connection.execute_many("INSERT INTO people(name) VALUES(%s)", [("1",), ("2",), ("3",)])

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

        query = "SELECT * FROM people LIMIT 1"
        retval = self.connection.get_row(query, cache=2)

        key = self.connection.cache.build_query_key(query)
        assert self.connection.cache.get(key), None

        time.sleep(3)
        assert self.connection.cache.get(key) == None
        
    def test_execute_many(self):

        self.connection.execute_many("INSERT INTO people(name) VALUES(%s)", [("john",), ("brad",), ("richard",)])
        
        is_in = self.connection.get_results("SELECT * FROM people WHERE name  IN ('john', 'brad', 'richard')")
        assert len(is_in) == 3

    def test_false_insert(self):
        self.assertRaises(ProgrammingError, self.connection.execute, "INSERT INTO there_is_no_table_like_this(name)  VALUES(%s)", "aaa")

    def test_zauto_commit(self):
        TestConfig.autocommit = False
        connection = Connection(TestConfig)
        connection.execute("BEGIN")
        connection.execute("INSERT INTO people(name) VALUES(%s)", ["yusufkoc"])
        is_in = connection.get_results("SELECT * FROM people WHERE id =%s", ["yusufkoc", ])
        assert len(is_in) == 0
        connection.execute("COMMIT")
        is_in = self.connection.get_results("SELECT * FROM people WHERE name = %s", ["yusufkoc", ])
        assert len(is_in) == 1


    def tearDown(self):
        #  self.connection.execute("TRUNCATE TABLE people")
        pass

if __name__ == '__main__':
    unittest.main()
