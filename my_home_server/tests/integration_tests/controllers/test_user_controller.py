from urllib import request, parse
import json
from urllib.error import HTTPError

from my_home_server.tests.integration_tests.base_test import BaseTest


class TestUserController(BaseTest):
    def setUp(self):
        super().setUp()

    def test_authenticate_endpoint_invalid_credentials(self):
        dto = {
            "username": "1",
            "password": "2"
        }

        response = self.client.post("/api/auth/authenticate", json=dto)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(401, response.status_code)
        self.assertEqual("Authentication failed for 1", response_dto["description"])
        self.assertEqual("INVALID_CREDENTIALS", response_dto["error"])
        self.assertEqual(401, response_dto["status_code"])

    def test_authenticate_endpoint(self):
        dto = {
            "username": "default",
            "password": "default"
        }

        response = self.client.post("/api/auth/authenticate", json=dto)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response_dto["access_token"])
