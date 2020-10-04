import unittest
from datetime import datetime

from my_home_server.services.product_service import ProductService


class TestProductService(unittest.TestCase):
    def setUp(self):
        self.service = ProductService(None, None, None, None)

    def test_fill_create_without_dto(self):
        self.service.fill_to_create(None, datetime.utcnow(), None)
