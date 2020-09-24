import json

from my_home_server.models.brand import Brand
from my_home_server.tests.integration_tests.base_test import BaseTest


class TestBrandController(BaseTest):

    def test_find_by_id(self):

        response = self.client.get("/api/brand/100", headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response_dto["id"])
        self.assertEqual("Brand 1", response_dto["name"])
        self.assertEqual(False, response_dto["is_private"])
        self.assertEqual(1, response_dto["created_by"]["id"])

    def test_find_by_id_without_token(self):
        response = self.client.get("/api/brand/100")
        self.assertEqual(403, response.status_code)

    def test_find_all(self):

        response = self.client.get("/api/brand/", headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(8, len(response_dto))
        self.assertEqual(100, response_dto[0]["id"])
        self.assertEqual("Brand 1", response_dto[0]["name"])
        self.assertEqual(False, response_dto[0]["is_private"])
        self.assertEqual(1, response_dto[0]["created_by"]["id"])

    def test_find_all_without_token(self):
        response = self.client.get("/api/brand/")
        self.assertEqual(403, response.status_code)

    def test_create_without_name(self):

        dto = {}

        response = self.client.post("/api/brand/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual(40016, response_dto["error_code"])
        self.assertEqual(Brand.__name__, response_dto["description"]["entity_name"])
        self.assertEqual(["name"], response_dto["description"]["required_fields"])

    def test_create(self):

        dto = {
            "name": "Test 1"
        }

        response = self.client.post("/api/brand/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual("Test 1", response_dto["name"])
        self.assertIsNotNone(response_dto["created_at"])
        self.assertEqual(1, response_dto["created_by"]["id"])

    def test_create_without_token(self):
        dto = {
            "name": "Test 1"
        }

        response = self.client.post("/api/brand/", json=dto)
        self.assertEqual(403, response.status_code)

    def test_update_without_instance(self):

        dto = {
            "id": 1,
            "name": "Test1"
        }

        response = self.client.put("/api/brand/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual(40005, response_dto["error_code"])
        self.assertEqual({"id": 1}, response_dto["description"]["entity_identifier"])
        self.assertEqual(Brand.__name__, response_dto["description"]["entity_name"])

    def test_update(self):

        dto = {
            "id": 100,
            "name": "Test1"
        }

        response = self.client.put("/api/brand/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual("Test1", response_dto["name"])

    def test_update_without_token(self):
        dto = {
            "name": "Test 1"
        }

        response = self.client.put("/api/brand/", json=dto)
        self.assertEqual(403, response.status_code)

    def test_delete(self):
        response = self.client.delete("/api/brand/100", headers=self.get_authentication_header())
        self.assertEqual(200, response.status_code)
        self.assertIsNone(self.db.session.query(Brand).get(100))

    def test_delete_without_permission(self):
        response = self.client.delete("/api/brand/106", headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual(40010, response_dto["error_code"])
        self.assertEqual({"id": 106}, response_dto["description"]["entity_identifier"])

    def test_delete_without_token(self):
        response = self.client.delete("/api/brand/106")
        self.assertEqual(403, response.status_code)

