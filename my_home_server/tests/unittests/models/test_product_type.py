import unittest

from my_home_server.models.product_type import ProductType
from my_home_server.models.user import User
from my_home_server.models.user_group import UserGroup

p1 = ProductType()
p1.id = 1

p2 = ProductType()
p2.id = 2
p2.parent_product_type = p1

p3 = ProductType()
p3.id = 3
p3.parent_product_type = p2


class TestProductType(unittest.TestCase):

    def test_equal_with_same_id(self):
        pr1 = ProductType()
        pr1.id = 1

        pr2 = ProductType()
        pr2.id = 1

        self.assertEqual(pr1, pr2)

    def test_equal_with_different_id(self):
        pr1 = ProductType()
        pr1.id = 1

        pr2 = ProductType()
        pr2.id = 132

        self.assertNotEqual(pr1, pr2)

    def test_get_root_parent_product_type_without_parent(self):
        self.assertEqual(None, p1.get_root_product_type())

    def test_get_root_parent_product_type(self):
        self.assertEqual(p1, p3.get_root_product_type())

    def test_get_root_parent_product_type_with_before(self):
        self.assertEqual(p2, p3.get_root_product_type(before_product_type=p1))

    def test_get_root_parent_product_type_with_before_some_item(self):
        self.assertEqual(None, p3.get_root_product_type(before_product_type=p2))

    def test_is_root_without_root(self):
        self.assertFalse(p2.is_root())

    def test_is_root_with_root(self):
        self.assertTrue(p1.is_root())
