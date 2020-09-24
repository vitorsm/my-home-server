import json

from my_home_server.models.purchase_list import PurchaseList
from my_home_server.tests.integration_tests.base_test import BaseTest


class TestPurchaseListController(BaseTest):
    def test_find_by_id(self):

        response = self.client.get("/api/purchase-list/1", headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response_dto["id"])
        self.assertEqual("List 1", response_dto["name"])
        self.assertEqual(2, len(response_dto["products"]))
        self.assertEqual(10, response_dto["products"][0]["id"])
        self.assertEqual("Product 10", response_dto["products"][0]["name"])

    def test_find_by_id_without_token(self):
        response = self.client.get("/api/purchase-list/1")
        self.assertEqual(403, response.status_code)

    def test_find_all(self):

        response = self.client.get("/api/purchase-list/", headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(6, len(response_dto))
        self.assertEqual(3, response_dto[1]["id"])
        self.assertEqual("List 3", response_dto[1]["name"])
        self.assertEqual(1, response_dto[1]["created_by"]["id"])

    def test_find_all_without_token(self):
        response = self.client.get("/api/purchase-list/")
        self.assertEqual(403, response.status_code)

    def test_create_without_name(self):

        dto = {}

        response = self.client.post("/api/purchase-list/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual(40019, response_dto["error_code"])
        self.assertEqual(PurchaseList.__name__, response_dto["description"]["entity_name"])
        self.assertEqual(["name"], response_dto["description"]["required_fields"])

    def test_create(self):

        dto = {
            "name": "Test 1"
        }

        response = self.client.post("/api/purchase-list/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual("Test 1", response_dto["name"])
        self.assertIsNotNone(response_dto["created_at"])
        self.assertEqual(1, response_dto["created_by"]["id"])

    def test_create_without_token(self):
        dto = {
            "name": "Test 1"
        }

        response = self.client.post("/api/purchase-list/", json=dto)
        self.assertEqual(403, response.status_code)

    def test_update_without_instance(self):

        dto = {
            "id": 1123,
            "name": "Test1"
        }

        response = self.client.put("/api/purchase-list/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual(40008, response_dto["error_code"])
        self.assertEqual({"id": 1123}, response_dto["description"]["entity_identifier"])
        self.assertEqual(PurchaseList.__name__, response_dto["description"]["entity_name"])

    def test_update_without_token(self):
        dto = {
            "name": "Test 1"
        }

        response = self.client.put("/api/purchase-list/", json=dto)
        self.assertEqual(403, response.status_code)

    def test_update(self):

        dto = {
            "id": 1,
            "name": "new_name",
            "products": [{
                "id": 11,
                "quantity": 2,
                "value": 123.2
            }]
        }

        response = self.client.put("/api/purchase-list/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual("new_name", response_dto["name"])
        self.assertEqual(1, len(response_dto["products"]))
        self.assertEqual(11, response_dto["products"][0]["id"])
        self.assertEqual(2, response_dto["products"][0]["quantity"])
        self.assertEqual(123.2, response_dto["products"][0]["value"])

    def test_delete(self):
        response = self.client.delete("/api/purchase-list/1", headers=self.get_authentication_header())
        self.assertEqual(200, response.status_code)
        self.assertIsNone(self.db.session.query(PurchaseList).get(1))

    def test_delete_without_permission(self):
        response = self.client.delete("/api/purchase-list/2", headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual(40013, response_dto["error_code"])
        self.assertEqual({"id": 2}, response_dto["description"]["entity_identifier"])

    def test_delete_without_token(self):
        response = self.client.delete("/api/purchase-list/1")
        self.assertEqual(403, response.status_code)

