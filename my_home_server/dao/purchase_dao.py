from typing import List

from my_home_server.dao.dao import DAO
from my_home_server.models.purchase import Purchase
from my_home_server.models.user import User


class PurchaseDAO(DAO):
    def find_all_by_user(self, user: User) -> List[Purchase]:
        return self.db.session.query(Purchase).find(Purchase.created_by == user)

    def find_by_id(self, purchase_id: int, current_user: User) -> Purchase:
        return self.db.session.query(Purchase).find(Purchase.id == purchase_id and Purchase.created_by == current_user)
