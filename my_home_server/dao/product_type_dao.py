from typing import List

from my_home_server.dao.dao import DAO
from my_home_server.models.product_type import ProductType
from my_home_server.models.user import User

from sqlalchemy import or_
from sqlalchemy.sql.expression import false


class ProductTypeDAO(DAO):
    def find_by_id(self, product_type_id: int, current_user: User) -> ProductType:
        return self.db.session.query(ProductType).filter(ProductType.id == product_type_id).\
            filter(or_(ProductType.is_private == false(), ProductType.created_by == current_user)).first()

    def find_by_product_type_parent(self, product_type_parent_id: int, current_user: User) -> List[ProductType]:
        return self.db.session.query(ProductType).filter(ProductType.parent_product_type.id == product_type_parent_id).\
            filter(or_(ProductType.is_private == false(), ProductType.created_by == current_user)).all()

    def find_allowed(self, current_user: User) -> List[ProductType]:
        return self.db.session.query(ProductType).filter(or_(ProductType.is_private == false(),
                                                             ProductType.created_by == current_user)).all()
