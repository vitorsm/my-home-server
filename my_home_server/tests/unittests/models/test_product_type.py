import unittest

from my_home_server.models.product_type import ProductType
from my_home_server.models.user import User
from my_home_server.models.user_group import UserGroup


class TestProductType(unittest.TestCase):

    def test_equal_with_same_id(self):
        p1 = ProductType()
        p1.id = 1

        p2 = ProductType()
        p2.id = 1

        self.assertEqual(p1, p2)

    def test_equal_with_different_id(self):
        p1 = ProductType()
        p1.id = 1

        p2 = ProductType()
        p2.id = 132

        self.assertNotEqual(p1, p2)