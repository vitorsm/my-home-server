from my_home_server.exceptions.invalid_dto_exception import InvalidDTOException
from my_home_server.exceptions.object_not_found_exception import ObjectNotFoundException
from my_home_server.models.purchase import Purchase
from my_home_server.models.purchase_list import PurchaseList
from my_home_server.models.user import User
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.services.purchase_list_service import PurchaseListService
from my_home_server.tests.integration_tests.base_test import BaseTest


class TestPurchaseListService(BaseTest):
    def setUp(self):
        super().setUp()
        self.service = self.dependency_injector.get(PurchaseListService)

    def test_find_by_id_not_exists(self):
        self.assertIsNone(self.service.find_by_id(1111))

    def test_find_by_id_without_permission(self):
        self.assertIsNone(self.service.find_by_id(6))

    def test_find_by_id(self):
        purchase_list = self.service.find_by_id(1)

        self.assertEqual(1, purchase_list.id)
        self.assertEqual("List 1", purchase_list.name)
        self.assertEqual(2, len(purchase_list.purchase_products))

    def test_create_from_dto(self):
        dto = {
            "name": "Test name",
            "purchase_products": [
                {
                    "name": "new_name",
                    "product_type": {"id": 100, "name": "new_product_type"},
                    "brand": {"id": 109},
                    "image_url": None,
                    "value": 12.2,
                    "quantity": 2
                }, {
                    "id": 1112,
                    "name": "new_name2",
                    "product_type": {"id": 101, "name": "new_product_type2"},
                    "brand": {"id": 109},
                    "image_url": None,
                    "value": 12.2,
                    "quantity": 2
                }
            ]
        }

        purchase_list = self.service.create_from_dto(dto)

        assert purchase_list in self.db.session

        self.assertEqual("Test name", purchase_list.name)
        self.assertEqual("new_name", purchase_list.purchase_products[0].product.name)
        self.assertEqual("new_name2", purchase_list.purchase_products[1].product.name)
        self.assertEqual("new_product_type2", purchase_list.purchase_products[1].product.product_type.name)
        self.assertEqual(2, purchase_list.purchase_products[1].quantity)

    def test_create_from_dto_without_name(self):
        dto = {
            "purchase_products": [
                {
                    "id": 1111,
                    "name": "new_name",
                    "product_type": {"id": 100, "name": "new_product_type"},
                    "brand": {"id": 109},
                    "image_url": None,
                    "value": 12.2,
                    "quantity": 2
                }, {
                    "id": 1112,
                    "name": "new_name2",
                    "product_type": {"id": 100, "name": "new_product_type"},
                    "brand": {"id": 109},
                    "image_url": None,
                    "value": 12.2,
                    "quantity": 2
                }
            ]
        }

        with self.assertRaises(InvalidDTOException) as exception:
            self.service.create_from_dto(dto)

        self.assertEqual(["name"], exception.exception.required_fields)
        self.assertEqual(PurchaseList.__name__, exception.exception.entity_name)

    def test_create_from_dto_without_products(self):
        dto = {
            "name": "Test name"
        }

        purchase_list = self.service.create_from_dto(dto)

        assert purchase_list in self.db.session

        self.assertEqual("Test name", purchase_list.name)

    def test_update_from_dto_without_name(self):
        dto = {
            "id": 1,
            "purchase_products": [
                {
                    "id": 1111,
                    "name": "new_name",
                    "product_type": {"id": 100, "name": "new_product_type"},
                    "brand": {"id": 109},
                    "image_url": None,
                    "value": 12.2,
                    "quantity": 2
                }, {
                    "id": 1112,
                    "name": "new_name2",
                    "product_type": {"id": 100, "name": "new_product_type"},
                    "brand": {"id": 109},
                    "image_url": None,
                    "value": 12.2,
                    "quantity": 2
                }
            ]
        }

        with self.assertRaises(InvalidDTOException) as exception:
            self.service.update_from_dto(dto)

        self.assertEqual(["name"], exception.exception.required_fields)
        self.assertEqual(PurchaseList.__name__, exception.exception.entity_name)

    def test_update_from_dto_with_new_product(self):
        dto = {
            "id": 3,
            "name": "Test name",
            "purchase_products": [
                {
                    "id": 1111,
                    "name": "new_name",
                    "product_type": {"id": 1111, "name": "new_product_type1"},
                    "brand": {"id": 109},
                    "image_url": None,
                    "value": 12.2,
                    "quantity": 1
                }, {
                    "id": 1112,
                    "name": "new_name2",
                    "product_type": {
                        "id": 1112,
                        "name": "new_product_type2",
                        "parent_product_type": {
                            "id": 1
                        }
                    },
                    "brand": {"id": 109},
                    "image_url": None,
                    "value": 12.1,
                    "quantity": 2
                }
            ]
        }

        self.service.update_from_dto(dto)

        purchase_list = self.db.session.query(PurchaseList).get(3)

        self.assertEqual("Test name", purchase_list.name)
        self.assertEqual(2, len(purchase_list.purchase_products))
        self.assertEqual(1111, purchase_list.purchase_products[0].product.id)
        self.assertEqual(1112, purchase_list.purchase_products[1].product.id)
        self.assertEqual("new_product_type1", purchase_list.purchase_products[0].product.product_type.name)
        self.assertEqual("new_product_type2", purchase_list.purchase_products[1].product.product_type.name)
        self.assertEqual(1, purchase_list.purchase_products[1].product.product_type.parent_product_type.id)
        self.assertEqual(12.2, purchase_list.purchase_products[0].estimated_value)
        self.assertEqual(12.1, purchase_list.purchase_products[1].estimated_value)
        self.assertEqual(1, purchase_list.purchase_products[0].quantity)
        self.assertEqual(2, purchase_list.purchase_products[1].quantity)

    def test_update_from_dto_without_permission(self):
        dto = {
            "id": 2,
            "name": "Test name",
            "purchase_products": [
                {
                    "id": 1111,
                    "name": "new_name",
                    "product_type": {"id": 100, "name": "new_product_type"},
                    "brand": {"id": 109},
                    "image_url": None,
                    "value": 12.2,
                    "quantity": 2
                }, {
                    "id": 1112,
                    "name": "new_name2",
                    "product_type": {"id": 100, "name": "new_product_type"},
                    "brand": {"id": 109},
                    "image_url": None,
                    "value": 12.2,
                    "quantity": 2
                }
            ]
        }

        with self.assertRaises(ObjectNotFoundException) as exception:
            self.service.update_from_dto(dto)

        self.assertEqual({"id": 2}, exception.exception.entity_identifier)
        self.assertEqual(PurchaseList.__name__, exception.exception.entity_name)

    def test_delete_by_id_without_permission(self):
        with self.assertRaises(ObjectNotFoundException) as exception:
            self.service.delete_by_id(2)

        self.assertEqual({"id": 2}, exception.exception.entity_identifier)
        self.assertEqual(PurchaseList.__name__, exception.exception.entity_name)

    def test_delete_by_id(self):
        self.service.delete_by_id(4)
        self.assertIsNone(self.db.session.query(PurchaseList).get(4))

    def test_find_all(self):
        user = self.db.session.query(User).get(5)
        AuthenticationContext.init_context(user)

        purchase_lists = self.service.find_all()

        self.assertEqual(2, len(purchase_lists))
        self.assertEqual(2, purchase_lists[0].id)
        self.assertEqual(6, purchase_lists[1].id)
