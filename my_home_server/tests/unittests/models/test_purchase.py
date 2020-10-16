import copy
import unittest

from my_home_server.models.product import Product
from my_home_server.models.purchase import Purchase
from my_home_server.models.purchase_product import PurchaseProduct
from my_home_server.models.purchase_list import PurchaseList
from my_home_server.models.purchase_list_product import PurchaseListProduct
from my_home_server.models.user import User
from my_home_server.models.user_group import UserGroup
from my_home_server.models.brand import Brand
from my_home_server.models.product_type import ProductType


product_type1 = ProductType()
product_type1.id = 1

product_type2 = ProductType()
product_type2.id = 2
product_type2.parent_product_type = product_type1

product_type3 = ProductType()
product_type3.id = 3

product_type4 = ProductType()
product_type4.id = 4
product_type4.parent_product_type = product_type3


product1 = Product()
product1.id = 1
product1.name = 'Test 1'
product1.product_type = product_type1
purchase_product1 = PurchaseProduct()
purchase_product1.product = product1
purchase_product1.value = 12.3
purchase_product1.quantity = 1

product2 = Product()
product2.id = 2
product2.name = 'Test 2'
product2.product_type = product_type2
purchase_product2 = PurchaseProduct()
purchase_product2.product = product2
purchase_product2.value = 1.5
purchase_product2.quantity = 21

product3 = Product()
product3.id = 3
product3.name = 'Test 3'
product3.product_type = product_type3
purchase_product3 = PurchaseProduct()
purchase_product3.product = product3
purchase_product3.value = 19
purchase_product3.quantity = 4

product4 = Product()
product4.id = 4
product4.name = 'Test 4'
product4.product_type = product_type4
purchase_product4 = PurchaseProduct()
purchase_product4.product = product4
purchase_product4.value = 12
purchase_product4.quantity = 1

product5 = Product()
product5.id = 5
product5.name = 'Test 4'
product5.product_type = product_type4
purchase_product5 = PurchaseProduct()
purchase_product5.product = product5
purchase_product5.value = 18.12
purchase_product5.quantity = 3


purchase_to_fill_total_value = Purchase()
purchase_to_fill_total_value.products = [purchase_product1, purchase_product2, purchase_product3,
                                         purchase_product4]

purchase_to_fill_total_value_without_products = Purchase()

purchase_to_test_get_product_types_values = Purchase()
purchase_to_test_get_product_types_values.products = [purchase_product1, purchase_product2, purchase_product3,
                                                      purchase_product4, purchase_product5]


class TestPurchase(unittest.TestCase):

    def test_equal_with_same_id(self):
        p1 = Purchase()
        p1.id = 1

        p2 = Purchase()
        p2.id = 1

        self.assertEqual(p1, p2)

    def test_equal_with_different_id(self):
        p1 = Purchase()
        p1.id = 1

        p2 = Purchase()
        p2.id = 132

        self.assertNotEqual(p1, p2)

    def test_fill_total_value_with_products(self):
        purchase_to_fill_total_value.fill_total_value()
        self.assertEqual(131.8, purchase_to_fill_total_value.total_value)

    def test_fill_total_value_without_products(self):
        purchase_to_fill_total_value_without_products.fill_total_value()
        self.assertEqual(0, purchase_to_fill_total_value_without_products.total_value)

    def test_get_product_types_and_values_without_product_type(self):
        p1 = Purchase()
        p1.id = 1

        product = Product()
        product.id = 1
        product.name = 'Test 1'

        pp = PurchaseProduct()
        pp.product = product
        pp.value = 12.3
        pp.quantity = 1

        p1.products = [pp]

        self.assertEqual([], p1.get_product_type_and_values())

    def test_get_product_types_and_values_without_data(self):
        p1 = Purchase()
        p1.id = 1
        p1.products = []

        self.assertEqual([], p1.get_product_type_and_values())

    def test_get_product_types_and_values_with_data(self):
        result = purchase_to_test_get_product_types_values.get_product_type_and_values()

        self.assertEqual(2, len(result))
        self.assertEqual(1, len(result[0]["children"]))
        self.assertEqual(1, len(result[1]["children"]))
        self.assertEqual(43.8, result[0]["value"])
        self.assertEqual(142.36, result[1]["value"])
        self.assertEqual(31.5, result[0]["children"][0]["value"])
        self.assertEqual(66.36, result[1]["children"][0]["value"])

