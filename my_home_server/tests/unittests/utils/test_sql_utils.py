import unittest

import my_home_server.utils.sql_utils as sql_utils


class TestSQLUtils(unittest.TestCase):

    def test_get_position_of_field_in_insert_query_without_parentheses(self):
        insert_query = "INSERT user "
        field = "test"

        self.assertEqual(-1, sql_utils.get_position_of_field_in_insert_query(insert_query, field))

    def test_get_position_of_field_in_insert_query_without_field(self):
        insert_query = "INSERT user (test)"
        field = ''

        self.assertEqual(-1, sql_utils.get_position_of_field_in_insert_query(insert_query, field))

    def test_get_position_of_field_in_insert_query_without_field_in_query(self):
        insert_query = "INSERT user (test)"
        field = 'name'

        self.assertEqual(-1, sql_utils.get_position_of_field_in_insert_query(insert_query, field))

    def test_get_position_of_field_in_insert_query_with_field_in_query(self):
        insert_query = "INSERT user (test, id, description, name, date)"
        field = 'name'

        self.assertEqual(3, sql_utils.get_position_of_field_in_insert_query(insert_query, field))

    def test_get_position_of_field_in_insert_query_without_columns(self):
        insert_query = "INSERT user ()"
        field = 'name'

        self.assertEqual(-1, sql_utils.get_position_of_field_in_insert_query(insert_query, field))

