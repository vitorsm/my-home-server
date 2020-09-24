import unittest

from my_home_server.exceptions.no_mapper_exception import NoMapperException
from my_home_server.mappers.mapper import Mapper


class TestMapper(unittest.TestCase):

    def test_get_mapper_with_invalid_type(self):

        with self.assertRaises(NoMapperException) as exception:
            mapper = Mapper.get_mapper("str")

        self.assertEqual("str", exception.exception.entity_name)
