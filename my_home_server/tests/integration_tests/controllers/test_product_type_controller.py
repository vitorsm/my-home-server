import json

from my_home_server.models.product_type import ProductType
from my_home_server.tests.integration_tests.base_test import BaseTest


class TestProductTypeController(BaseTest):

    def test_find_by_id(self):
        response = self.client.get("/api/product-type/1", headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response_dto["id"])
        self.assertEqual("ProductType1", response_dto["name"])
        self.assertEqual("Product Type 1", response_dto["description"])
        self.assertEqual(False, response_dto["is_private"])
        self.assertEqual(1, response_dto["created_by"]["id"])

    def test_find_by_id_without_token(self):
        response = self.client.get("/api/product-type/1")
        self.assertEqual(403, response.status_code)

    def test_find_all(self):

        response = self.client.get("/api/product-type/", headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(9, len(response_dto))
        self.assertEqual(5, response_dto[3]["id"])
        self.assertEqual("ProductType41", response_dto[3]["name"])
        self.assertEqual("Product Type 41", response_dto[3]["description"])
        self.assertEqual(True, response_dto[3]["is_private"])
        self.assertEqual("ProductType4", response_dto[3]["parent_product_type"]["name"])

    def test_find_all_without_token(self):
        response = self.client.get("/api/product-type/")
        self.assertEqual(403, response.status_code)

    def test_create(self):

        dto = {
            "name": "Test 1"
        }

        response = self.client.post("/api/product-type/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual("Test 1", response_dto["name"])
        self.assertIsNotNone(response_dto["created_at"])
        self.assertEqual(1, response_dto["created_by"]["id"])

    def test_create_without_name(self):

        dto = {}

        response = self.client.post("/api/product-type/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual(40017, response_dto["error_code"])
        self.assertEqual(ProductType.__name__, response_dto["description"]["entity_name"])
        self.assertEqual(["name"], response_dto["description"]["required_fields"])

    def test_create_without_token(self):
        dto = {
            "name": "Test 1"
        }

        response = self.client.post("/api/product-type/", json=dto)
        self.assertEqual(403, response.status_code)

    def test_update_without_instance(self):

        dto = {
            "id": 1123,
            "name": "Test1"
        }

        response = self.client.put("/api/product-type/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual(40006, response_dto["error_code"])
        self.assertEqual({"id": 1123}, response_dto["description"]["entity_identifier"])
        self.assertEqual(ProductType.__name__, response_dto["description"]["entity_name"])

    def test_update(self):

        dto = {
            "id": 6,
            "name": "new_name",
            "parent_product_type": None
        }

        response = self.client.put("/api/product-type/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual("new_name", response_dto["name"])
        self.assertIsNone(response_dto["parent_product_type"])

    def test_update_without_token(self):
        dto = {
            "name": "Test 1"
        }

        response = self.client.put("/api/product-type/", json=dto)
        self.assertEqual(403, response.status_code)

    def test_delete(self):
        response = self.client.delete("/api/product-type/4", headers=self.get_authentication_header())
        self.assertEqual(200, response.status_code)
        self.assertIsNone(self.db.session.query(ProductType).get(4))

    def test_delete_without_permission(self):
        response = self.client.delete("/api/product-type/2", headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual(40011, response_dto["error_code"])
        self.assertEqual({"id": 2}, response_dto["description"]["entity_identifier"])

    def test_delete_without_token(self):
        response = self.client.delete("/api/product-type/1")
        self.assertEqual(403, response.status_code)
