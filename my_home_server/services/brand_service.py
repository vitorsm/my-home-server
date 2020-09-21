from datetime import datetime
from typing import List, Optional

from my_home_server.dao.brand_dao import BrandDAO
from my_home_server.mappers.mapper import Mapper
from my_home_server.models.brand import Brand
from my_home_server.security.authentication_context import AuthenticationContext


class BrandService(object):
    def __init__(self, brand_dao: BrandDAO):
        self.brand_dao = brand_dao
        self.mapper = Mapper.get_mapper(Brand.__name__)

    def find_or_create(self, dto: dict) -> Optional[Brand]:
        if not dto or dto.get("id"):
            return None

        brand = self.find_by_id(dto.get("id"))

        if not brand:
            brand = self.create_by_dto(dto)

        return brand

    def find_by_id(self, brand_id: int) -> Brand:
        return self.brand_dao.find_by_id(brand_id, AuthenticationContext.get_current_user())

    def find_all(self) -> List[Brand]:
        return self.brand_dao.find_all(AuthenticationContext.get_current_user())

    def create_by_dto(self, dto: dict):
        self.mapper.validate_dto(dto)

        brand = self.mapper.to_object(dto)
        brand.created_at = datetime.utcnow()
        brand.created_by = AuthenticationContext.get_current_user()

        self.brand_dao.add(brand)

        return brand
