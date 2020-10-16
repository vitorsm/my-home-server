import unittest

from my_home_server.models.product import Product
from my_home_server.models.purchase_list import PurchaseList
from my_home_server.models.purchase_list_product import PurchaseListProduct
from my_home_server.models.user import User
from my_home_server.models.user_group import UserGroup
from my_home_server.models.brand import Brand
from my_home_server.models.product_type import ProductType


class TestPurchaseListProduct(unittest.TestCase):
    def test_calculated_value_without_value(self):
        purchase_list_product = PurchaseListProduct()
        purchase_list_product.quantity = 12

        self.assertEqual(0, purchase_list_product.calculated_value)

    def test_calculated_value_with_value(self):
        purchase_list_product = PurchaseListProduct()
        purchase_list_product.quantity = 11
        purchase_list_product.estimated_value = 3

        self.assertEqual(33, purchase_list_product.calculated_value)

    def test_calculated_value_with_value2(self):
        purchase_list_product = PurchaseListProduct()
        purchase_list_product.quantity = 11
        purchase_list_product.estimated_value = 0

        self.assertEqual(0, purchase_list_product.calculated_value)
