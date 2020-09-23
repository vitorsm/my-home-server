from typing import List, Optional

from sqlalchemy import or_
from sqlalchemy.sql.expression import false

from my_home_server.dao.dao import DAO
from my_home_server.models.product import Product
from my_home_server.models.user import User


class ProductDAO(DAO):
    def find_all(self, current_user: User) -> List[Product]:
        return self.db.session.query(Product).\
            filter(Product.created_by == current_user).filter(Product.is_private == false()).all()

    def find_by_id(self, product_id: int, current_user: User) -> Optional[Product]:
        return self.db.session.query(Product).\
            filter(Product.id == product_id).filter(or_(Product.created_by == current_user,
                                                        Product.is_private == false())).first()
