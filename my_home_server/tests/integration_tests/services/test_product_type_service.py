from my_home_server.exceptions.invalid_dto_exception import InvalidDTOException
from my_home_server.exceptions.object_not_found import ObjectNotFoundException
from my_home_server.models.product_type import ProductType
from my_home_server.models.user import User
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.services.product_type_service import ProductTypeService
from my_home_server.tests.integration_tests.base_test import BaseTest


class TestProductTypeService(BaseTest):
    def setUp(self):
        super().setUp()
        self.service = self.dependency_injector.get(ProductTypeService)

    def test_find_by_id_without_permission(self):
        self.assertIsNone(self.service.find_by_id(2))

    def test_find_by_id(self):
        self.assertEqual(1, self.service.find_by_id(1).id)

    def test_find_all(self):
        user = self.db.session.query(User).get(4)
        AuthenticationContext.init_context(user)

        product_types = self.service.find_all()

        self.assertEqual(6, len(product_types))
        self.assertNotIn(3, [p.id for p in product_types])

    def test_create_by_dto_without_name(self):
        dto = {
            "name": None,
            "description": "Test description"
        }

        with self.assertRaises(InvalidDTOException) as exception:
            self.service.create_by_dto(dto)

        self.assertEqual(["name"], exception.exception.required_fields)
        self.assertEqual(ProductType.__name__, exception.exception.entity_name)

    def test_create_by_dto(self):
        dto = {
            "name": "Name",
            "description": "Test description"
        }

        product_type = self.service.create_by_dto(dto)

        assert product_type in self.db.session

        self.assertEqual("Name", product_type.name)
        self.assertEqual("Test description", product_type.description)

    def test_create_by_dto_with_parents(self):
        dto = {
            "name": "Name",
            "description": "Test description",
            "parent_product_type": {
                "name": "Test 2",
                "parent_product_type": {
                    "id": 1
                }
            }
        }

        product_type = self.service.create_by_dto(dto)

        assert product_type in self.db.session

        self.assertEqual("Name", product_type.name)
        self.assertEqual("Test description", product_type.description)
        self.assertEqual("Test 2", product_type.parent_product_type.name)
        self.assertEqual(1, product_type.parent_product_type.parent_product_type.id)

    def test_update_by_dto_without_id(self):
        dto = {
            "name": "Name",
            "description": "Test description",
            "parent_product_type": {
                "name": "Test 21",
                "parent_product_type": {
                    "id": 1
                }
            }
        }

        with self.assertRaises(InvalidDTOException) as exception:
            self.service.update_by_dto(dto)

        self.assertEqual(["id"], exception.exception.required_fields)
        self.assertEqual(ProductType.__name__, exception.exception.entity_name)

    def test_update_by_dto_without_permission(self):
        dto = {
            "id": 2,
            "name": "Name",
            "description": "Test description",
            "parent_product_type": {
                "name": "Test 21",
                "parent_product_type": {
                    "id": 1
                }
            }
        }

        with self.assertRaises(ObjectNotFoundException) as exception:
            self.service.update_by_dto(dto)

        self.assertEqual(ProductType.__name__, exception.exception.entity_name)
        self.assertEqual({"id": 2}, exception.exception.entity_identifier)

    def test_update_by_dto(self):
        dto = {
            "id": 3,
            "name": "new_name",
            "description": "Test description",
            "parent_product_type": {
                "name": "Test 2",
                "parent_product_type": {
                    "id": 4
                }
            }
        }

        product_type = self.service.update_by_dto(dto)

        self.assertEqual("new_name", product_type.name)
        self.assertEqual("Test description", product_type.description)
        self.assertEqual("Test 2", product_type.parent_product_type.name)
        self.assertEqual(4, product_type.parent_product_type.parent_product_type.id)

    def test_delete_by_id_without_permission(self):

        with self.assertRaises(ObjectNotFoundException) as exception:
            self.service.delete_by_id(2)

        self.assertEqual(ProductType.__name__, exception.exception.entity_name)
        self.assertEqual({"id": 2}, exception.exception.entity_identifier)

    def test_delete_by_id(self):

        self.service.delete_by_id(4)

        self.assertIsNone(self.db.session.query(ProductType).get(4))
        self.assertIsNone(self.db.session.query(ProductType).get(5))
        self.assertIsNone(self.db.session.query(ProductType).get(6))

    def test_find_or_create_without_id(self):
        dto = {
            "name": "other_name",
            "description": "Test description",
            "parent_product_type": {
                "name": "Test 2",
                "parent_product_type": {
                    "id": 4
                }
            }
        }

        product_type = self.service.find_or_create_by_dto(dto)

        self.assertIsNone(product_type)

    def test_find_or_create_not_creating(self):
        dto = {
            "id": 3,
            "name": "other_name",
            "description": "Test description",
            "parent_product_type": {
                "name": "Test 2",
                "parent_product_type": {
                    "id": 4
                }
            }
        }

        product_type = self.service.find_or_create_by_dto(dto)

        self.assertEqual(3, product_type.id)
        self.assertNotEqual("other_name", product_type.id)

    def test_find_or_create_creating(self):
        dto = {
            "id": 300,
            "name": "other_name",
            "description": "Test description",
            "parent_product_type": {
                "name": "Test 2",
                "parent_product_type": {
                    "id": 4
                }
            }
        }

        product_type = self.service.find_or_create_by_dto(dto)

        self.assertEqual(300, product_type.id)
        self.assertNotEqual("other_name", product_type.id)