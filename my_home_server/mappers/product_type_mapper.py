from typing import Optional

from my_home_server.dao.product_type_dao import ProductTypeDAO
from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.mappers.user_mapper import UserMapper
from my_home_server.models.product_type import ProductType
from my_home_server.security.authentication_context import AuthenticationContext


class ProductTypeMapper(MapperInterface):

    def __init__(self, product_type_dao: ProductTypeDAO, user_mapper: UserMapper):
        self.user_mapper = user_mapper
        self.product_type_dao = product_type_dao

    def get_error_code_when_dto_invalid_to_insert(self):
        return ErrorCode.INVALID_INPUT_CREATE_PRODUCT_TYPE

    def get_error_code_when_dto_invalid_to_update(self):
        return ErrorCode.INVALID_INPUT_UPDATE_PRODUCT_TYPE

    def to_dto(self, obj: ProductType) -> Optional[dict]:
        if not obj:
            return None

        return {
            "id": obj.id,
            "name": obj.name,
            "description": obj.description,
            "parent_product_type": self.to_dto(obj.parent_product_type) if obj.parent_product_type else None,
            "is_private": obj.is_private,
            "created_by": self.user_mapper.to_dto(obj.created_by),
            "created_at": obj.created_at
        }

    def to_object(self, dto: dict, not_update: bool = False) -> Optional[object]:
        if not dto:
            return None

        product_type = None
        found = False
        if dto.get("id"):
            product_type = self.product_type_dao.find_by_id(dto.get("id"), AuthenticationContext.get_current_user())
            found = product_type is not None

        if not found:
            product_type = ProductType()
            product_type.id = dto.get("id")
            product_type.created_by = self.user_mapper.to_object(dto.get("created_by"))
            product_type.created_at = dto.get("created_at")
            product_type.is_private = dto.get("is_private")

        if not found or not not_update:
            product_type.name = dto.get("name")
            product_type.parent_product_type = self.to_object(dto.get("parent_product_type"), not_update=True)
            product_type.description = dto.get("description")

        return product_type

    def get_required_fields_to_insert(self):
        return ["name"]

    def get_required_fields_to_update(self):
        return ["id", "name"]

    def get_entity_name(self):
        return ProductType.__name__
