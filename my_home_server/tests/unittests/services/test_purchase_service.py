import unittest

from my_home_server.services.purchase_service import PurchaseService


purchases_to_test = []

class TestPurchaseService(unittest.TestCase):
    def setUp(self):
        self.service = PurchaseService(None, None, None, None)
