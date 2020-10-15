import unittest
from datetime import datetime

from my_home_server.models.purchase import Purchase
from my_home_server.services.purchase_service import PurchaseService


purchase1 = Purchase()
purchase1.created_at = datetime(2020, 10, 1)
purchase1.total_value = 12
purchase2 = Purchase()
purchase2.created_at = datetime(2020, 10, 12)
purchase2.total_value = 13
purchase3 = Purchase()
purchase3.created_at = datetime(2020, 11, 5)
purchase3.total_value = 45
purchase4 = Purchase()
purchase4.created_at = datetime(2020, 11, 30)
purchase4.total_value = 31
purchase5 = Purchase()
purchase5.created_at = datetime(2020, 12, 15)
purchase5.total_value = 42

purchases_to_test_group_by_month = [purchase1, purchase2, purchase3, purchase4, purchase5]


class TestPurchaseService(unittest.TestCase):
    def setUp(self):
        self.service = PurchaseService(None, None, None, None, None)

    def test_group_purchase_by_month_without_data(self):
        grouped_purchase = self.service.group_purchases_by_month(list())
        self.assertIsNone(grouped_purchase)

    def test_group_purchase_by_month(self):
        grouped_purchase = self.service.group_purchases_by_month(purchases_to_test_group_by_month)

        self.assertEqual(3, len(grouped_purchase))

        key1 = list(grouped_purchase.keys())[0]
        key2 = list(grouped_purchase.keys())[1]
        key3 = list(grouped_purchase.keys())[2]

        self.assertEqual(datetime(2020, 10, 1), datetime.fromtimestamp(key1))
        self.assertEqual(datetime(2020, 11, 5), datetime.fromtimestamp(key2))
        self.assertEqual(datetime(2020, 12, 15), datetime.fromtimestamp(key3))

        self.assertEqual(2, len(grouped_purchase[key1]))
        self.assertEqual(2, len(grouped_purchase[key2]))
        self.assertEqual(1, len(grouped_purchase[key3]))
