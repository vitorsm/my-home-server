from my_home_server.services.brand_service import BrandService
from my_home_server.tests.integration_tests.base_test import BaseTest


class TestBrandService(BaseTest):
    def setUp(self):
        super().setUp()
        self.service = self.dependency_injector.get(BrandService)

    def test_find_brand_by_id_with_permission(self):
        brand = self.service.find_by_id(2)

        self.assertIsNotNone(brand)
        self.assertEqual(2, brand.id)

    def test_find_brand_by_id_without_permission(self):
        brand = self.service.find_by_id(6)
        self.assertIsNone(brand)
