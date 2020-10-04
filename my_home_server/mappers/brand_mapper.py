from typing import Optional

from my_home_server.dao.brand_dao import BrandDAO
from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.mappers.user_mapper import UserMapper
from my_home_server.models.brand import Brand
from my_home_server.security.authentication_context import AuthenticationContext


class BrandMapper(MapperInterface):
    def __init__(self, brand_dao: BrandDAO, user_mapper: UserMapper):
        self.brand_dao = brand_dao
        self.user_mapper = user_mapper

    def get_error_code_when_dto_invalid_to_insert(self):
        return ErrorCode.INVALID_INPUT_CREATE_BRAND

    def get_error_code_when_dto_invalid_to_update(self):
        return ErrorCode.INVALID_INPUT_UPDATE_BRAND

    def to_object(self, dto: dict, not_update: bool = False) -> Optional[Brand]:
        if not dto:
            return None

        brand = None
        found = False
        if dto.get("id"):
            brand = self.brand_dao.find_by_id(dto.get("id"), AuthenticationContext.get_current_user())
            found = brand is not None

        if not found:
            brand = Brand()
            brand.id = dto.get("id")
            brand.created_at = dto.get("created_at")
            brand.is_private = dto.get("is_private")
            brand.created_by = self.user_mapper.to_object(dto.get("created_by"), not_update=True)

        if not found or not not_update:
            brand.name = dto.get("name")

        return brand

    def get_required_fields_to_insert(self):
        return ["name"]

    def get_required_fields_to_update(self):
        return ["id", "name"]

    def get_entity_name(self):
        return Brand.__name__

    def to_dto(self, brand: Brand) -> Optional[dict]:
        if not brand:
            return None

        return {
            "id": brand.id,
            "name": brand.name,
            "is_private": brand.is_private,
            "created_by": self.user_mapper.to_dto(brand.created_by),
            "created_at": brand.created_at
        }
