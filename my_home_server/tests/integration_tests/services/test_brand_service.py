
from my_home_server.exceptions.invalid_dto_exception import InvalidDTOException
from my_home_server.exceptions.object_not_found import ObjectNotFoundException
from my_home_server.models.brand import Brand
from my_home_server.models.user import User
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.services.brand_service import BrandService
from my_home_server.tests.integration_tests.base_test import BaseTest


class TestBrandService(BaseTest):
    def setUp(self):
        super().setUp()
        self.service = self.dependency_injector.get(BrandService)

    def test_find_brand_by_id_with_permission(self):
        brand = self.service.find_by_id(102)

        self.assertIsNotNone(brand)
        self.assertEqual(102, brand.id)

    def test_find_brand_by_id_without_permission(self):
        brand = self.service.find_by_id(106)
        self.assertIsNone(brand)

    def test_create_brand_without_name(self):
        dto = {
            "name": None
        }

        with self.assertRaises(InvalidDTOException) as exception:
            self.service.create_by_dto(dto)

        self.assertEqual(["name"], exception.exception.required_fields)
        self.assertEqual(Brand.__name__, exception.exception.entity_name)

    def test_create_brand(self):
        dto = {
            "name": "Test brand"
        }

        brand = self.service.create_by_dto(dto)

        assert brand in self.db.session

        self.assertEqual("Test brand", brand.name)

    def test_update_brand_without_name(self):
        dto = {
            "id": 100,
            "name": None
        }

        with self.assertRaises(InvalidDTOException) as exception:
            self.service.update_by_dto(dto)

        self.assertEqual(Brand.__name__, exception.exception.entity_name)
        self.assertEqual(["name"], exception.exception.required_fields)

    def test_update_brand_without_permission(self):
        dto = {
            "id": 106,
            "name": "Test brand"
        }

        with self.assertRaises(ObjectNotFoundException) as exception:
            self.service.update_by_dto(dto)

        self.assertEqual(Brand.__name__, exception.exception.entity_name)
        self.assertEqual({"id": 106}, exception.exception.entity_identifier)

    def test_update_brand(self):
        new_name = "Test brand"
        dto = {
            "id": 100,
            "name": new_name
        }

        self.service.update_by_dto(dto)
        brand = self.service.find_by_id(100)

        self.assertEqual(new_name, brand.name)

    def test_find_or_create_by_dto_without_id(self):
        dto = {
            "id": 0,
            "name": "new_name"
        }

        brand = self.service.find_or_create_by_dto(dto)

        self.assertIsNone(brand)

    def test_find_or_create_by_dto_creating(self):
        dto = {
            "id": 10001,
            "name": "new_name"
        }

        brand = self.service.find_or_create_by_dto(dto)

        self.assertEqual(10001, brand.id)
        self.assertEqual("new_name", brand.name)

    def test_find_or_create_by_dto_not_creating(self):
        dto = {
            "id": 100,
            "name": "other"
        }

        brand = self.service.find_or_create_by_dto(dto)

        self.assertEqual(100, brand.id)
        self.assertNotEqual("other", brand.name)

    def test_find_all(self):
        user = self.db.session.query(User).get(4)
        AuthenticationContext.init_context(user)

        brands = self.service.find_all()

        self.assertEqual(8, len(brands))
        self.assertEqual({100, 102, 103, 106, 107, 108, 109, 110}, set([b.id for b in brands]))

    def test_delete_by_id_without_permission(self):
        with self.assertRaises(ObjectNotFoundException) as exception:
            self.service.delete_by_id(106)

        self.assertEqual(Brand.__name__, exception.exception.entity_name)
        self.assertEqual({"id": 106}, exception.exception.entity_identifier)

    def test_delete_by_id_without(self):
        self.service.delete_by_id(105)

        self.assertIsNone(self.db.session.query(Brand).get(105))
