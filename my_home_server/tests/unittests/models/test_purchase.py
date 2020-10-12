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

product1 = Product()
product1.id = 1
product1.name = 'Test 1'
purchase_product1 = PurchaseProduct()
purchase_product1.product = product1
purchase_product1.value = 12.3
purchase_product1.quantity = 1

product2 = Product()
product2.id = 2
product2.name = 'Test 2'
purchase_product2 = PurchaseProduct()
purchase_product2.product = product2
purchase_product2.value = 1.5
purchase_product2.quantity = 21

product3 = Product()
product3.id = 3
product3.name = 'Test 3'
purchase_product3 = PurchaseProduct()
purchase_product3.product = product3
purchase_product3.value = 19
purchase_product3.quantity = 4

product4 = Product()
product4.id = 4
product4.name = 'Test 4'
purchase_product4 = PurchaseProduct()
purchase_product4.product = product4
purchase_product4.value = 12
purchase_product4.quantity = 1


purchase_to_fill_total_value = Purchase()
purchase_to_fill_total_value.products = [purchase_product1, purchase_product2, purchase_product3,
                                         purchase_product4]

purchase_to_fill_total_value_without_products = Purchase()


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
