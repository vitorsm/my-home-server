import unittest

from my_home_server.models.brand import Brand
from my_home_server.models.user import User
from my_home_server.models.user_group import UserGroup

class TestBrand(unittest.TestCase):

    def test_equal_with_same_id(self):
        b1 = Brand()
        b1.id = 1

        b2 = Brand()
        b2.id = 1

        self.assertEqual(b1, b2)

    def test_equal_with_different_id(self):
        b1 = Brand()
        b1.id = 1

        b2 = Brand()
        b2.id = 11

        self.assertNotEqual(b1, b2)
