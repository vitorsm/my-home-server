from typing import List

from my_home_server.dao.dao import DAO
from my_home_server.models.product_type import ProductType
from my_home_server.models.user import User


class ProductTypeDAO(DAO):
    def find_by_id(self, product_type_id: int, current_user: User) -> ProductType:
        return self.db.session.query(ProductType).find(ProductType.id == product_type_id and
                                                       (ProductType.is_private == True or
                                                        ProductType.created_by == current_user))

    def find_by_product_type_parent(self, product_type_parent_id: int, current_user: User) -> List[ProductType]:
        return self.db.session.query(ProductType).find(ProductType.parent_product_type.id == product_type_parent_id and
                                                       (ProductType.is_private == True or
                                                        ProductType.created_by == current_user))

    def find_allowed(self, current_user: User) -> List[ProductType]:
        return self.db.session.query(ProductType).find(ProductType.is_private == False
                                                       or ProductType.created_by == current_user)
