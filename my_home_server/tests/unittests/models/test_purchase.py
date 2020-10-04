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
