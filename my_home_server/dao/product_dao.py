from typing import List, Optional

from my_home_server.dao.dao import DAO
from my_home_server.models.product import Product
from my_home_server.models.user import User


class ProductDAO(DAO):
    def find_all(self, current_user: User) -> List[Product]:
        return self.db.session.query(Product).find(Product.created_by == current_user and Product.is_private == False)

    def find_by_id(self, product_id: int, current_user: User) -> Optional[Product]:
        return self.db.session.query(Product).find(Product.id == product_id and (Product.created_by == current_user or
                                                                                 Product.is_private == False))
