from typing import List, Optional

from my_home_server.dao.dao import DAO
from my_home_server.models.purchase_list import PurchaseList
from my_home_server.models.user import User


class PurchaseListDAO(DAO):
    def find_all_by_user(self, user: User) -> List[PurchaseList]:
        return self.db.session.query(PurchaseList).find(PurchaseList.created_by == user)

    def find_by_id(self, purchase_list_id: int, current_user: User) -> Optional[PurchaseList]:
        return self.db.session.query(PurchaseList).find(PurchaseList.id == purchase_list_id and
                                                        PurchaseList.created_by == current_user)
