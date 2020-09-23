
from my_home_server.services.user_service import UserService
from my_home_server.tests.integration_tests.base_test import BaseTest


import my_home_server.security.authentication_utils as authentication_utils


class TestAuthenticationUtils(BaseTest):
    def setUp(self):
        super().setUp()
        self.user_service = self.dependency_injector.get(UserService)

    def test_authenticate(self):
        authentication_utils.authenticate("default", "default", self.user_service)

    def test_identity(self):
        user = authentication_utils.identity({"identity": 1}, self.user_service)

        self.assertEqual(1, user.id)
