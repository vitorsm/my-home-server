from datetime import datetime
from typing import List

from my_home_server.dao.dao import DAO
from my_home_server.models.purchase import Purchase
from my_home_server.models.user import User

from sqlalchemy import and_


class PurchaseDAO(DAO):
    def find_all_by_user(self, user: User) -> List[Purchase]:
        return self.db.session.query(Purchase).filter(Purchase.created_by == user).all()

    def find_by_id(self, purchase_id: int, current_user: User) -> Purchase:
        return self.db.session.query(Purchase).\
            filter(and_(Purchase.id == purchase_id, Purchase.created_by == current_user)).first()

    def find_by_period(self, start_date: datetime, end_date: datetime, user: User) -> List[Purchase]:
        return self.db.session.query(Purchase).filter(Purchase.created_by == user)\
            .filter(Purchase.created_at.between(start_date, end_date)).all()
