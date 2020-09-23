import unittest

from my_home_server.mappers.user_group_mapper import UserGroupMapper


class TestUserGroupMapper(unittest.TestCase):
    def setUp(self):
        self.mapper = UserGroupMapper()

    def test_to_obj(self):
        dto = {
            "id": 1,
            "name": "user_group_test"
        }

        user_group = self.mapper.to_object(dto)

        self.assertEqual(1, user_group.id)
        self.assertEqual("user_group_test", user_group.name)
