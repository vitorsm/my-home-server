from typing import List

from sqlalchemy import or_
from sqlalchemy.sql.expression import false

from my_home_server.dao.dao import DAO
from my_home_server.models.brand import Brand
from my_home_server.models.user import User


class BrandDAO(DAO):
    def find_all(self, current_user: User) -> List[Brand]:
        return self.db.session.query(Brand).filter(or_(Brand.created_by == current_user,
                                                       Brand.is_private == false())).all()

    def find_by_id(self, brand_id: int, current_user: User) -> Brand:
        return self.db.session.query(Brand).filter(Brand.id == brand_id).\
            filter(or_(Brand.is_private == false(), Brand.created_by == current_user)).first()
