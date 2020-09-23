from my_home_server.exceptions.authentication_exception import AuthenticationException
from my_home_server.exceptions.duplicate_entry_exception import DuplicateEntryException
from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.exceptions.invalid_dto_exception import InvalidDTOException
from my_home_server.exceptions.object_not_found import ObjectNotFoundException
from my_home_server.exceptions.permission_exception import PermissionException, Actions
from my_home_server.models.user import User
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.security.password_encryption import PasswordEncryption
from my_home_server.services.user_service import UserService
from my_home_server.tests.integration_tests.base_test import BaseTest


class TestUserService(BaseTest):

    def setUp(self):
        super().setUp()
        self.service = self.dependency_injector.get(UserService)

    def test_create_user_from_dto_without_name(self):
        dto = {
            "name": None,
            "login": "testName",
            "password": "12345"
        }

        with self.assertRaises(InvalidDTOException) as exception:
            self.service.create_from_dto(dto)

        self.assertEqual(["name"], exception.exception.required_fields)
        self.assertEqual(User.__name__, exception.exception.entity_name)

    def test_create_user_from_dto(self):
        dto = {
            "name": "NameTest",
            "login": "testName",
            "password": "12345"
        }

        created_user = self.service.create_from_dto(dto)

        assert created_user in self.db.session

    def test_create_user_from_dto_with_duplicate_login(self):
        dto = {
            "name": "duplicate_name",
            "login": "duplicate_login",
            "password": "12345"
        }

        created_user = self.service.create_from_dto(dto)
        assert created_user in self.db.session

        with self.assertRaises(DuplicateEntryException) as exception:
            self.service.create_from_dto(dto)

        self.assertEqual(User.__name__, exception.exception.entity)
        self.assertEqual("login", exception.exception.field)
        self.assertEqual(ErrorCode.USER_LOGIN_ALREADY_EXISTS, exception.exception.error_code)
        self.assertEqual("duplicate_login", exception.exception.value)

    def test_get_current_user(self):
        self.assertIsNotNone(AuthenticationContext.get_current_user())

    def test_find_user_by_id(self):
        user = self.service.find_by_id(1)

        self.assertIsNotNone(user)
        self.assertEqual(1, user.id)
        self.assertIsNotNone(user.user_group)

    def test_find_user_by_id_when_return_is_none(self):
        user = self.service.find_by_id(100)
        self.assertIsNone(user)

    def test_authenticate_valid_credentials(self):
        user = self.service.authenticate("default", "default")
        self.assertIsNotNone(user)

    def test_authenticate_invalid_login(self):
        invalid_login = "invalid_login"
        with self.assertRaises(AuthenticationException) as exception:
            self.service.authenticate(invalid_login, "default")

        self.assertEqual(invalid_login, exception.exception.login)

    def test_authenticate_invalid_password(self):
        invalid_password = "invalid_password"
        with self.assertRaises(AuthenticationException) as exception:
            self.service.authenticate("login", invalid_password)

        self.assertEqual("login", exception.exception.login)

    def test_update_user_by_dto_without_id(self):
        dto = {
            "id": 0,
            "name": "new_name",
            "login": "vitor",
            "password": "new_pass"
        }

        with self.assertRaises(InvalidDTOException) as exception:
            self.service.update_from_dto(dto)

        self.assertEqual(["id"], exception.exception.required_fields)
        self.assertEqual(User.__name__, exception.exception.entity_name)

    def test_update_user_by_dto_without_permission(self):
        dto = {
            "id": 2,
            "name": "new_name",
            "login": "vitor",
            "password": "new_pass"
        }

        with self.assertRaises(PermissionException) as exception:
            self.service.update_from_dto(dto)

        self.assertEqual(Actions.UPDATE, exception.exception.action)
        self.assertEqual(User.__name__, exception.exception.entity)

    def test_update_user_by_dto_invalid_id(self):
        dto = {
            "id": 290,
            "name": "new_name",
            "login": "vitor",
            "password": "new_pass"
        }

        user = User()
        user.id = 290

        AuthenticationContext.init_context(user)

        with self.assertRaises(ObjectNotFoundException) as exception:
            self.service.update_from_dto(dto)

        self.assertEqual({"id": 290}, exception.exception.entity_identifier)
        self.assertEqual(User.__name__, exception.exception.entity_name)

    def test_update_pass_and_name_user_by_dto(self):
        dto = {
            "id": 2,
            "name": "new_name",
            "login": "vitor",
            "password": "new_pass"
        }

        user = self.service.find_by_id(2)
        AuthenticationContext.init_context(user)

        self.service.update_from_dto(dto)

        user = self.service.find_by_id(2)

        self.assertEqual("new_name", user.name)
        self.assertTrue(PasswordEncryption.check_encrypted_password("new_pass", user.password))

    def test_update_name_user_by_dto(self):
        dto = {
            "id": 2,
            "name": "new_name",
            "login": "vitor",
            "password": None
        }

        user = self.service.find_by_id(2)
        AuthenticationContext.init_context(user)

        self.service.update_from_dto(dto)

        user = self.service.find_by_id(2)

        self.assertEqual("new_name", user.name)
