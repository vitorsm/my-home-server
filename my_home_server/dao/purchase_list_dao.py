from typing import List, Optional

from my_home_server.dao.dao import DAO
from my_home_server.models.purchase_list import PurchaseList
from my_home_server.models.user import User

from sqlalchemy import and_


class PurchaseListDAO(DAO):
    def find_all_by_user(self, user: User) -> List[PurchaseList]:
        return self.db.session.query(PurchaseList).filter(PurchaseList.created_by == user).all()

    def find_by_id(self, purchase_list_id: int, current_user: User) -> Optional[PurchaseList]:
        return self.db.session.query(PurchaseList).filter(and_(PurchaseList.id == purchase_list_id,
                                                          PurchaseList.created_by == current_user)).first()
