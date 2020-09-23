from datetime import datetime
from typing import List, Optional

from my_home_server.dao.brand_dao import BrandDAO
from my_home_server.exceptions.object_not_found import ObjectNotFoundException
from my_home_server.mappers.mapper import Mapper
from my_home_server.models.brand import Brand
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.utils.sql_utils import transaction


class BrandService(object):

    def __init__(self, brand_dao: BrandDAO):
        self.brand_dao = brand_dao
        self.mapper = Mapper.get_mapper(Brand.__name__)

    @transaction
    def create(self, brand: Brand):
        brand.created_at = datetime.utcnow()
        brand.created_by = AuthenticationContext.get_current_user()

        self.brand_dao.add(brand)

        return brand

    @transaction
    def create_by_dto(self, dto: dict):
        self.mapper.validate_dto_to_insert(dto)

        brand = self.mapper.to_object(dto)

        return self.create(brand)

    @transaction
    def fetch_or_create(self, brand: Brand) -> Optional[Brand]:
        if not brand:
            return None

        new_brand = None

        if brand.id:
            new_brand = self.find_by_id(brand.id)

        if not new_brand:
            new_brand = self.create(brand)
        else:
            self.brand_dao.expunge(brand)

        return new_brand

    @transaction
    def update_by_dto(self, dto: dict):
        self.mapper.validate_dto_to_update(dto)

        brand = self.brand_dao.find_by_id(dto.get("id"), AuthenticationContext.get_current_user())

        if not brand:
            raise ObjectNotFoundException(Brand.__name__, {"id": dto.get("id")})

        self.mapper.to_object(dto, brand)
        self.brand_dao.commit()

    @transaction
    def delete_by_id(self, brand_id: int):
        brand = self.find_by_id(brand_id)

        if not brand:
            raise ObjectNotFoundException(Brand.__name__, {"id": brand_id})

        self.brand_dao.delete(brand)

    @transaction
    def find_or_create_by_dto(self, dto: dict) -> Optional[Brand]:
        if not dto or not dto.get("id"):
            return None

        brand = self.find_by_id(dto.get("id"))

        if not brand:
            brand = self.create_by_dto(dto)

        return brand

    def find_by_id(self, brand_id: int) -> Brand:
        return self.brand_dao.find_by_id(brand_id, AuthenticationContext.get_current_user())

    def find_all(self) -> List[Brand]:
        return self.brand_dao.find_all(AuthenticationContext.get_current_user())

    def commit(self):
        self.brand_dao.commit()
