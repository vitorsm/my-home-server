import json

from my_home_server.models.purchase import Purchase
from my_home_server.tests.integration_tests.base_test import BaseTest


class TestPurchaseController(BaseTest):
    def test_find_by_id(self):

        response = self.client.get("/api/purchase/1", headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response_dto["id"])
        self.assertEqual("Purchase 1", response_dto["name"])
        self.assertEqual(1, response_dto["created_by"]["id"])
        self.assertEqual(7, response_dto["purchase_list"]["id"])
        self.assertEqual("List 7", response_dto["purchase_list"]["name"])
        self.assertEqual(4, len(response_dto["products"]))
        self.assertEqual("Product 13", response_dto["products"][0]["name"])
        self.assertEqual(1, response_dto["products"][0]["quantity"])
        self.assertEqual(6.5, response_dto["products"][0]["value"])

    def test_find_by_id_without_token(self):
        response = self.client.get("/api/purchase/1")
        self.assertEqual(403, response.status_code)

    def test_find_all(self):

        response = self.client.get("/api/purchase/", headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(5, len(response_dto))
        self.assertEqual(1, response_dto[0]["id"])
        self.assertEqual("Purchase 1", response_dto[0]["name"])
        self.assertEqual(1, response_dto[0]["created_by"]["id"])

    def test_find_all_without_token(self):
        response = self.client.get("/api/purchase/")
        self.assertEqual(403, response.status_code)

    def test_create_empty(self):

        dto = {}

        response = self.client.post("/api/purchase/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response_dto["created_by"]["id"])
        self.assertIsNone(response_dto["name"])

    def test_create(self):

        dto = {
            "name": "Test 1"
        }

        response = self.client.post("/api/purchase/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response_dto["created_by"]["id"])
        self.assertEqual("Test 1", response_dto["name"])

    def test_create_without_token(self):
        dto = {
            "name": "Test 1"
        }

        response = self.client.post("/api/purchase/", json=dto)
        self.assertEqual(403, response.status_code)

    def test_update_without_instance(self):

        dto = {
            "id": 1123,
            "name": "Test1"
        }

        response = self.client.put("/api/purchase/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual(40009, response_dto["error_code"])
        self.assertEqual({"id": 1123}, response_dto["description"]["entity_identifier"])
        self.assertEqual(Purchase.__name__, response_dto["description"]["entity_name"])

    def test_update_without_token(self):
        dto = {
            "name": "Test 1"
        }

        response = self.client.put("/api/purchase/", json=dto)
        self.assertEqual(403, response.status_code)

    def test_update(self):

        dto = {
            "id": 1,
            "name": "new_name",
            "purchase_list": {"id": 10},
            "products": [{
                "id": 13,
                "quantity": 10,
                "value": 1.1
            }]
        }

        response = self.client.put("/api/purchase/", json=dto, headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual("new_name", response_dto["name"])
        self.assertEqual("List 10", response_dto["purchase_list"]["name"])
        self.assertEqual(1, len(response_dto["products"]))
        self.assertEqual("Product 13", response_dto["products"][0]["name"])

    def test_delete(self):
        response = self.client.delete("/api/purchase/1", headers=self.get_authentication_header())
        self.assertEqual(200, response.status_code)
        self.assertIsNone(self.db.session.query(Purchase).get(1))

    def test_delete_without_permission(self):
        response = self.client.delete("/api/purchase/2", headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(400, response.status_code)
        self.assertEqual(40014, response_dto["error_code"])
        self.assertEqual({"id": 2}, response_dto["description"]["entity_identifier"])

    def test_delete_without_token(self):
        response = self.client.delete("/api/purchase/1")
        self.assertEqual(403, response.status_code)

    def test_get_response_dto_without_permission(self):
        response = self.client.get("/api/purchase/monthly-spend")

        self.assertEqual(403, response.status_code)

    def test_get_response_dto_without_data(self):
        response = self.client.get("/api/purchase/monthly-spend", headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_dto))

    def test_get_response_dto(self):
        response = self.client.get("/api/purchase/monthly-spend?start-date=2020-09-22&end-date=2020-12-30",
                                   headers=self.get_authentication_header())
        response_dto = json.loads(response.data.decode())

        self.assertEqual(200, response.status_code)
        
        self.assertEqual(4, len(response_dto))

        self.assertEqual(2020, response_dto[0].get("year"))
        self.assertEqual(9, response_dto[0].get("month"))
        self.assertEqual(146, response_dto[0].get("value"))

        self.assertEqual(2020, response_dto[1].get("year"))
        self.assertEqual(10, response_dto[1].get("month"))
        self.assertEqual(12, response_dto[1].get("value"))

        self.assertEqual(2020, response_dto[2].get("year"))
        self.assertEqual(11, response_dto[2].get("month"))
        self.assertEqual(31, response_dto[2].get("value"))

        self.assertEqual(2020, response_dto[3].get("year"))
        self.assertEqual(12, response_dto[3].get("month"))
        self.assertEqual(56, response_dto[3].get("value"))
