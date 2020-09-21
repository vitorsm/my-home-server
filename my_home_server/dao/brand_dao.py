from typing import List

from my_home_server.dao.dao import DAO
from my_home_server.models.brand import Brand
from my_home_server.models.user import User


class BrandDAO(DAO):
    def find_all(self, current_user: User) -> List[Brand]:
        return self.db.session.query(Brand).find(Brand.created_by == current_user)

    def find_by_id(self, brand_id: int, current_user: User) -> Brand:
        return self.db.session.query(Brand).find(Brand.id == brand_id and (Brand.is_private == False or
                                                                           Brand.created_by == current_user))
