import unittest
from datetime import datetime

import my_home_server.utils.date_utils as date_utils


class TestDateUtils(unittest.TestCase):

    def test_check_is_datetime_without_data(self):
        self.assertFalse(date_utils.check_if_str_date_has_time(None))

    def test_check_is_datetime_with_hour(self):
        self.assertTrue(date_utils.check_if_str_date_has_time("2020-10-14T09:35:18"))

    def test_check_is_datetime_with_hour_and_microseconds(self):
        self.assertTrue(date_utils.check_if_str_date_has_time("2020-10-14T09:35:18.707261"))

    def test_check_is_datetime_without_hour(self):
        self.assertFalse(date_utils.check_if_str_date_has_time("2020-10-14T09"))

    def test_check_is_datetime_without_hour_wrong(self):
        self.assertFalse(date_utils.check_if_str_date_has_time("2020-10-14T09:"))

    def test_convert_date_without_data(self):
        self.assertIsNone(date_utils.from_str_to_date(None))

    def test_convert_date_without_hour(self):
        expected_date = datetime(2020, 10, 1)
        result = date_utils.from_str_to_date("2020-10-01")

        self.assertEqual(expected_date, result)

    def test_convert_date_with_hour(self):
        expected_date = datetime(2020, 10, 14, 9, 35, 18)
        result = date_utils.from_str_to_date("2020-10-14T09:35:18")

        self.assertEqual(expected_date, result)

    def test_convert_date_with_hour_and_microseconds(self):
        expected_date = datetime(2020, 10, 14, 9, 35, 18, 707261)
        result = date_utils.from_str_to_date("2020-10-14T09:35:18.707261")

        self.assertEqual(expected_date, result)

    def test_convert_date_without_and_microseconds_and_tz(self):
        expected_date = datetime(2020, 4, 1, 23, 47, 41, 414)
        result = date_utils.from_str_to_date("2020-04-01T23:47:41.414Z")

        self.assertEqual(expected_date, result)
