from datetime import datetime
from typing import List, Optional

from my_home_server.dao.brand_dao import BrandDAO
from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.exceptions.object_not_found_exception import ObjectNotFoundException

from my_home_server.mappers.brand_mapper import BrandMapper
from my_home_server.models.brand import Brand
from my_home_server.models.user import User
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.utils.sql_utils import transaction


class BrandService(object):

    def __init__(self, brand_dao: BrandDAO, brand_mapper: BrandMapper):
        self.brand_dao = brand_dao
        self.mapper = brand_mapper

    @transaction
    def create(self, brand: Brand) -> Brand:
        BrandService.fill_to_create(brand, datetime.utcnow(), AuthenticationContext.get_current_user())

        self.brand_dao.add(brand)

        return brand

    @transaction
    def create_from_dto(self, dto: dict):
        self.mapper.validate_dto_to_insert(dto)

        brand = self.mapper.to_object(dto)

        return self.create(brand)

    @transaction
    def update_from_dto(self, dto: dict):
        self.mapper.validate_dto_to_update(dto)

        brand = self.brand_dao.find_by_id(dto.get("id"), AuthenticationContext.get_current_user())

        if not brand:
            raise ObjectNotFoundException(ErrorCode.BRAND_TO_UPDATE_NOT_FOUND,  Brand.__name__, {"id": dto.get("id")})

        brand = self.mapper.to_object(dto)

        self.brand_dao.update(brand)

        return brand

    @transaction
    def delete_by_id(self, brand_id: int):
        brand = self.find_by_id(brand_id)

        if not brand:
            raise ObjectNotFoundException(ErrorCode.BRAND_TO_DELETE_NOT_FOUND, Brand.__name__, {"id": brand_id})

        self.brand_dao.delete(brand)

    @transaction
    def find_or_create_from_dto(self, dto: dict) -> Optional[Brand]:
        if not dto or not dto.get("id"):
            return None

        brand = self.find_by_id(dto.get("id"))

        if not brand:
            brand = self.create_from_dto(dto)

        return brand

    @staticmethod
    def fill_to_create(brand: Brand, created_at: datetime, created_by: User):
        if not brand:
            return

        if not brand.created_by:
            brand.created_at = created_at
            brand.created_by = created_by

    def find_by_id(self, brand_id: int) -> Brand:
        return self.brand_dao.find_by_id(brand_id, AuthenticationContext.get_current_user())

    def find_all(self) -> List[Brand]:
        return self.brand_dao.find_all(AuthenticationContext.get_current_user())

    def commit(self):
        self.brand_dao.commit()
