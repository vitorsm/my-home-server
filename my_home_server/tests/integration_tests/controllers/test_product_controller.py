import json

from my_home_server.models.product import Product
from my_home_server.tests.integration_tests.base_test import BaseTest


class TestProductController(BaseTest):

    def test_find_by_id(self):

        response = self.client.get("/api/product/1", headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response_dto["id"])
        self.assertEqual("Product 1", response_dto["name"])
        self.assertEqual(True, response_dto["is_private"])
        self.assertEqual(1, response_dto["created_by"]["id"])
        self.assertEqual(108, response_dto["brand"]["id"])
        self.assertEqual(8, response_dto["product_type"]["id"])

    def test_find_by_id_without_token(self):
        response = self.client.get("/api/product/1")
        self.assertEqual(403, response.status_code)

    def test_find_all(self):

        response = self.client.get("/api/product/", headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(14, len(response_dto))
        self.assertEqual(1, response_dto[0]["id"])
        self.assertEqual("Product 1", response_dto[0]["name"])
        self.assertEqual(True, response_dto[0]["is_private"])
        self.assertEqual(1, response_dto[0]["created_by"]["id"])

    def test_find_all_without_token(self):
        response = self.client.get("/api/product/")
        self.assertEqual(403, response.status_code)

    def test_create_without_name(self):

        dto = {}

        response = self.client.post("/api/product/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual(40018, response_dto["error_code"])
        self.assertEqual(Product.__name__, response_dto["description"]["entity_name"])
        self.assertEqual(["name"], response_dto["description"]["required_fields"])

    def test_create(self):

        dto = {
            "name": "Test 1"
        }

        response = self.client.post("/api/product/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual("Test 1", response_dto["name"])
        self.assertIsNotNone(response_dto["created_at"])
        self.assertEqual(1, response_dto["created_by"]["id"])

    def test_create_without_token(self):
        dto = {
            "name": "Test 1"
        }

        response = self.client.post("/api/product/", json=dto)
        self.assertEqual(403, response.status_code)

    def test_update_without_instance(self):

        dto = {
            "id": 1123,
            "name": "Test1"
        }

        response = self.client.put("/api/product/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual(40007, response_dto["error_code"])
        self.assertEqual({"id": 1123}, response_dto["description"]["entity_identifier"])
        self.assertEqual(Product.__name__, response_dto["description"]["entity_name"])

    def test_update_without_token(self):
        dto = {
            "name": "Test 1"
        }

        response = self.client.put("/api/product/", json=dto)
        self.assertEqual(403, response.status_code)

    def test_update(self):

        dto = {
            "id": 1,
            "name": "new_name"
        }

        response = self.client.put("/api/product/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual("new_name", response_dto["name"])

    def test_delete(self):
        response = self.client.delete("/api/product/1", headers=self.get_authentication_header())
        self.assertEqual(200, response.status_code)
        self.assertIsNone(self.db.session.query(Product).get(1))

    def test_delete_without_permission(self):
        response = self.client.delete("/api/product/2", headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual(40012, response_dto["error_code"])
        self.assertEqual({"id": 2}, response_dto["description"]["entity_identifier"])

    def test_delete_without_token(self):
        response = self.client.delete("/api/product/1")
        self.assertEqual(403, response.status_code)

