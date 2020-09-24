from my_home_server.exceptions.invalid_dto_exception import InvalidDTOException
from my_home_server.exceptions.object_not_found_exception import ObjectNotFoundException
from my_home_server.models.product import Product
from my_home_server.models.user import User
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.services.product_service import ProductService
from my_home_server.tests.integration_tests.base_test import BaseTest


class TestProductService(BaseTest):
    def setUp(self):
        super().setUp()
        self.service = self.dependency_injector.get(ProductService)

    def test_find_product_by_id_not_exists(self):
        self.assertIsNone(self.service.find_by_id(190))

    def test_find_product_by_id_without_permission(self):
        self.assertIsNone(self.service.find_by_id(2))

    def test_find_all(self):
        AuthenticationContext.init_context(self.db.session.query(User).get(6))
        products = self.service.find_all()

        self.assertEqual(11, len(products))

    def test_find_product_by_id(self):
        product = self.service.find_by_id(1)

        self.assertEqual(1, product.id)
        self.assertEqual(8, product.product_type.id)
        self.assertEqual(108, product.brand.id)

    def test_find_product_by_id_with_null_fields(self):
        product = self.service.find_by_id(5)

        self.assertEqual(5, product.id)
        self.assertIsNone(product.product_type)
        self.assertIsNone(product.brand)

    def test_create_from_dto_without_name(self):
        dto = {
            "product_type": None,
            "brand": None,
            "image_url": None
        }

        with self.assertRaises(InvalidDTOException) as exception:
            self.service.create_from_dto(dto)

        self.assertEqual(["name"], exception.exception.required_fields)
        self.assertEqual(Product.__name__, exception.exception.entity_name)

    def test_create_from_dto(self):
        dto = {
            "name": "Name test",
            "product_type": None,
            "brand": None,
            "image_url": None
        }

        product = self.service.create_from_dto(dto)

        assert product in self.db.session
        product = self.db.session.query(Product).get(product.id)

        self.assertEqual("Name test", product.name)

    def test_create_from_dto_with_new_product_type(self):
        dto = {
            "name": "Name test",
            "product_type": {"name": "new_product_type_name"},
            "brand": None,
            "image_url": None
        }

        product = self.service.create_from_dto(dto)

        assert product in self.db.session
        product = self.db.session.query(Product).get(product.id)

        self.assertEqual("new_product_type_name", product.product_type.name)

    def test_create_from_dto_with_new_brand(self):
        dto = {
            "name": "Name test",
            "product_type": None,
            "brand": {"name": "new_brand_name"},
            "image_url": None
        }

        product = self.service.create_from_dto(dto)

        assert product in self.db.session
        product = self.db.session.query(Product).get(product.id)

        self.assertEqual("new_brand_name", product.brand.name)

    def test_create_from_dto_with_brand_and_product_type(self):
        dto = {
            "name": "Name test 2",
            "product_type": {"id": 8},
            "brand": {"id": 108},
            "image_url": None
        }

        product = self.service.create_from_dto(dto)

        assert product in self.db.session
        product = self.db.session.query(Product).get(product.id)

        self.assertEqual("Name test 2", product.name)
        self.assertEqual(8, product.product_type.id)
        self.assertEqual(108, product.brand.id)

    def test_update_from_dto_without_id_and_name(self):
        dto = {
            "product_type": None,
            "brand": None,
            "image_url": None
        }

        with self.assertRaises(InvalidDTOException) as exception:
            self.service.update_from_dto(dto)

        self.assertEqual(["id", "name"], exception.exception.required_fields)
        self.assertEqual(Product.__name__, exception.exception.entity_name)

    def test_update_from_dto_without_name(self):
        dto = {
            "id": 1,
            "product_type": None,
            "brand": None,
            "image_url": None
        }

        with self.assertRaises(InvalidDTOException) as exception:
            self.service.update_from_dto(dto)

        self.assertEqual(["name"], exception.exception.required_fields)
        self.assertEqual(Product.__name__, exception.exception.entity_name)

    def test_update_from_dto(self):
        dto = {
            "id": 1,
            "name": "new_name",
            "product_type": {"id": 100, "name": "new_product_type"},
            "brand": {"id": 109},
            "image_url": None
        }

        self.service.update_from_dto(dto)
        product = self.db.session.query(Product).get(1)

        self.assertEqual("new_name", product.name)
        self.assertEqual("new_product_type", product.product_type.name)
        self.assertEqual(109, product.brand.id)
        self.assertEqual("Brand 9", product.brand.name)

    def test_update_from_dto_fields_none(self):
        dto = {
            "id": 1,
            "name": "new_name",
            "image_url": None
        }

        self.service.update_from_dto(dto)
        product = self.db.session.query(Product).get(1)

        self.assertEqual("new_name", product.name)
        self.assertIsNone(product.product_type)
        self.assertIsNone(product.brand)

    def test_update_from_dto_without_permission(self):
        dto = {
            "id": 2,
            "name": "Name test",
            "product_type": None,
            "brand": None,
            "image_url": None
        }

        with self.assertRaises(ObjectNotFoundException) as exception:
            self.service.update_from_dto(dto)

        self.assertEqual(Product.__name__, exception.exception.entity_name)
        self.assertEqual({"id": 2}, exception.exception.entity_identifier)

    def test_delete_without_permission(self):
        with self.assertRaises(ObjectNotFoundException) as exception:
            self.service.delete_by_id(2)

        self.assertEqual(Product.__name__, exception.exception.entity_name)
        self.assertEqual({"id": 2}, exception.exception.entity_identifier)

    def test_delete(self):
        self.service.delete_by_id(4)
        self.assertIsNone(self.db.session.query(Product).get(4))

    def test_find_or_create_without_id(self):
        dto = {
            "name": "new_name",
            "product_type": {"id": 100, "name": "new_product_type"},
            "brand": {"id": 109},
            "image_url": None
        }

        self.assertIsNone(self.service.find_or_create_from_dto(dto))

    def test_find_or_create_creating(self):
        dto = {
            "id": 1111,
            "name": "new_name",
            "product_type": {"id": 100, "name": "new_product_type"},
            "brand": {"id": 109},
            "image_url": None
        }

        product = self.service.find_or_create_from_dto(dto)

        assert product in self.db.session

        self.assertEqual(100, product.product_type.id)
        self.assertEqual(109, product.brand.id)

    def test_find_or_create_not_creating(self):
        dto = {
            "id": 1,
            "name": "new_name",
            "product_type": {"id": 100, "name": "new_product_type"},
            "brand": {"id": 109},
            "image_url": None
        }

        product = self.service.find_or_create_from_dto(dto)

        self.assertEqual(1, product.id)
        self.assertEqual(8, product.product_type.id)
        self.assertEqual(108, product.brand.id)

    def test_fetch_or_create_without_value(self):
        self.assertIsNone(self.service.fetch_or_create(None))

    def test_fetch_or_create_with_value(self):
        product = self.db.session.query(Product).get(40)
        new_product = self.service.fetch_or_create(product)

        assert product not in self.db.session
        
        self.assertEqual(product, new_product)
