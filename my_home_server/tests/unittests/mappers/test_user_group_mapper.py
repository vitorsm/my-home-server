import unittest

from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.exceptions.invalid_dto_exception import InvalidDTOException
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

    def test_invalid_user_group_dto_to_insert(self):
        dto = {
            "id": 1
        }

        with self.assertRaises(InvalidDTOException) as exception:
            self.mapper.validate_dto_to_insert(dto)

        self.assertEqual(ErrorCode.INVALID_INPUT_CREATE_USER_GROUP, exception.exception.error_code)
        self.assertEqual(["name"], exception.exception.required_fields)

    def test_invalid_user_group_dto_to_update(self):
        dto = {
        }

        with self.assertRaises(InvalidDTOException) as exception:
            self.mapper.validate_dto_to_update(dto)

        self.assertEqual(ErrorCode.INVALID_INPUT_UPDATE_USER_GROUP, exception.exception.error_code)
        self.assertEqual(["id", "name"], exception.exception.required_fields)


