from urllib import request, parse
import json
from urllib.error import HTTPError

from my_home_server.models.user import User
from my_home_server.tests.integration_tests.base_test import BaseTest


class TestUserController(BaseTest):

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

    def test_find_user_by_id(self):

        response = self.client.get("/api/user/2", headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual("Vitor", response_dto["name"])
        self.assertEqual("vitor", response_dto["login"])
        self.assertEqual(1, response_dto["user_group"]["id"])

    def test_create_without_name_and_login(self):

        dto = {
            "password": "test"
        }

        response = self.client.post("/api/user/", json=dto)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual(40021, response_dto["error_code"])
        self.assertEqual(User.__name__, response_dto["description"]["entity_name"])
        self.assertEqual(["name", "login"], response_dto["description"]["required_fields"])

    def test_create_duplicate(self):
        dto = {
            "login": "vitor",
            "name": "Vitor",
            "password": "test"
        }

        response = self.client.post("/api/user/", json=dto)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual(40003, response_dto["error_code"])
        self.assertEqual(User.__name__, response_dto["description"]["entity"])
        self.assertEqual("login", response_dto["description"]["field"])
        self.assertEqual("vitor", response_dto["description"]["value"])

    def test_create(self):

        dto = {
            "login": "test1",
            "name": "Test1",
            "password": "test"
        }

        response = self.client.post("/api/user/", json=dto)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual("test1", response_dto["login"])
        self.assertIsNotNone(response_dto["created_at"])

        credential_dto = {
            "username": "test1",
            "password": "test"
        }

        response = self.client.post("/api/auth/authenticate", json=credential_dto)
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertIsNotNone(response_dto["access_token"])

    def test_update_without_instance(self):

        dto = {
            "id": 1123,
            "login": "test1",
            "name": "Test1",
            "password": "test"
        }

        response = self.client.put("/api/user/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual(40015, response_dto["error_code"])
        self.assertEqual(User.__name__, response_dto["description"]["entity_name"])
        self.assertEqual({"id": 1123}, response_dto["description"]["entity_identifier"])

    def test_update(self):

        dto = {
            "id": 1,
            "login": "test1",
            "name": "Test1",
            "password": "test"
        }

        response = self.client.put("/api/user/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual("default", response_dto["login"])
        self.assertEqual("Test1", response_dto["name"])
