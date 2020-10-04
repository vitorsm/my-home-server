from my_home_server.exceptions.object_not_found_exception import ObjectNotFoundException
from my_home_server.models.purchase import Purchase
from my_home_server.models.user import User
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.services.purchase_service import PurchaseService
from my_home_server.tests.integration_tests.base_test import BaseTest


class TestPurchaseService(BaseTest):
    def setUp(self):
        super().setUp()
        self.service = self.dependency_injector.get(PurchaseService)

    def test_find_by_id_without_permission(self):
        self.assertIsNone(self.service.find_by_id(2))

    def test_find_by_id(self):
        purchase = self.service.find_by_id(1)

        self.assertEqual("Purchase 1", purchase.name)
        self.assertEqual("List 7", purchase.purchase_list.name)
        self.assertEqual("List 7", purchase.purchase_list.name)
        self.assertEqual([13, 14, 15, 16], [pp.product.id for pp in purchase.purchase_list.purchase_products])
        self.assertEqual([13, 14, 15, 16], [pp.product.id for pp in purchase.products])

    def test_find_all(self):
        user = self.db.session.query(User).get(4)
        AuthenticationContext.init_context(user)

        purchases = self.service.find_all()

        self.assertEqual(2, len(purchases))
        self.assertEqual("Purchase 3", purchases[1].name)
        self.assertEqual([13, 14], [pp.product.id for pp in purchases[1].purchase_list.purchase_products])
        self.assertEqual([], [pp.product.id for pp in purchases[1].products])

    def test_create_from_dto_with_empty_dto(self):
        dto = {}
        purchase = self.service.create_from_dto(dto)
        assert purchase in self.db.session

        self.assertEqual(AuthenticationContext.get_current_user(), purchase.created_by)

    def test_create_from_dto_without_name(self):
        dto = {
            "purchase_list": {"id": 7},
            "products": [
                {
                    "id": 13,
                    "value": 12,
                    "quantity": 2
                }, {
                    "name": "new_product",
                    "value": 10,
                    "quantity": 1
                }
            ]
        }

        purchase = self.service.create_from_dto(dto)

        assert purchase in self.db.session

        self.assertIsNone(purchase.name)
        self.assertEqual(2, len(purchase.products))
        self.assertEqual("Product 13", purchase.products[0].product.name)

    def test_create_from_dto_without_products(self):
        dto = {
            "name": "Purchase name test",
            "purchase_list": {"id": 7}
        }

        purchase = self.service.create_from_dto(dto)

        assert purchase in self.db.session

        self.assertEqual("List 7", purchase.purchase_list.name)
        self.assertEqual("Purchase name test", purchase.name)

    def test_create_from_dto_with_id(self):
        dto = {
            "id": 111,
            "name": "Purchase name test",
            "purchase_list": {"id": 7}
        }

        purchase = self.service.create_from_dto(dto)

        assert purchase in self.db.session

        self.assertNotEqual(1, purchase.id)

    def test_delete_by_id_without_permission(self):
        with self.assertRaises(ObjectNotFoundException) as exception:
            self.service.delete_by_id(2)

        self.assertEqual({"id": 2}, exception.exception.entity_identifier)
        self.assertEqual(Purchase.__name__, exception.exception.entity_name)

    def test_delete_by_id(self):
        self.service.delete_by_id(7)

        self.assertIsNone(self.db.session.query(Purchase).get(7))

    def test_update_from_dto_without_permission(self):
        dto = {
            "id": 3,
            "name": "new_name",
            "purchase_list": {"id": 7}
        }

        with self.assertRaises(ObjectNotFoundException) as exception:
            self.service.update_from_dto(dto)

        self.assertEqual(Purchase.__name__, exception.exception.entity_name)
        self.assertEqual({"id": 3}, exception.exception.entity_identifier)

    def test_update_from_dto(self):
        dto = {
            "id": 4,
            "name": "new_name",
            "purchase_list": {"id": 7},
            "products": [
                {
                    "id": 13,
                    "value": 12,
                    "quantity": 2
                }, {
                    "name": "new_product",
                    "value": 10,
                    "quantity": 1
                }
            ]
        }

        self.service.update_from_dto(dto)
        purchase = self.db.session.query(Purchase).get(4)

        self.assertEqual("new_name", purchase.name)
        self.assertEqual("List 7", purchase.purchase_list.name)
        self.assertEqual(2, len(purchase.products))
        self.assertEqual(2, purchase.products[0].quantity)
        self.assertEqual(12, purchase.products[0].value)
        self.assertEqual("Product 13", purchase.products[0].product.name)
        self.assertEqual(1, purchase.products[1].quantity)
        self.assertEqual(10, purchase.products[1].value)
        self.assertEqual("new_product", purchase.products[1].product.name)

    def test_update_from_dto_with_purchase_list_none(self):
        dto = {
            "id": 4,
            "name": "new_name",
            "products": [
                {
                    "id": 13,
                    "value": 12,
                    "quantity": 2
                }, {
                    "name": "new_product",
                    "value": 10,
                    "quantity": 1
                }
            ]
        }

        self.service.update_from_dto(dto)
        purchase = self.db.session.query(Purchase).get(4)

        self.assertEqual("new_name", purchase.name)
        self.assertIsNone(purchase.purchase_list)
        self.assertEqual(2, len(purchase.products))
        self.assertEqual(2, purchase.products[0].quantity)
        self.assertEqual(12, purchase.products[0].value)
        self.assertEqual("Product 13", purchase.products[0].product.name)
        self.assertEqual(1, purchase.products[1].quantity)
        self.assertEqual(10, purchase.products[1].value)
        self.assertEqual("new_product", purchase.products[1].product.name)

