from typing import Optional

from my_home_server.dao.product_dao import ProductDAO
from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.mappers.brand_mapper import BrandMapper
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.mappers.product_type_mapper import ProductTypeMapper
from my_home_server.mappers.user_mapper import UserMapper
from my_home_server.models.product import Product
from my_home_server.security.authentication_context import AuthenticationContext


class ProductMapper(MapperInterface):
    def __init__(self, product_dao: ProductDAO, product_type_mapper: ProductTypeMapper, brand_mapper: BrandMapper,
                 user_mapper: UserMapper):
        self.product_type_mapper = product_type_mapper
        self.brand_mapper = brand_mapper
        self.user_mapper = user_mapper
        self.product_dao = product_dao

    def get_error_code_when_dto_invalid_to_insert(self):
        return ErrorCode.INVALID_INPUT_CREATE_PRODUCT

    def get_error_code_when_dto_invalid_to_update(self):
        return ErrorCode.INVALID_INPUT_UPDATE_PRODUCT

    def to_dto(self, obj: Product) -> Optional[dict]:
        if not obj:
            return None

        return {
            "id": obj.id,
            "name": obj.name,
            "product_type": self.product_type_mapper.to_dto(obj.product_type),
            "brand": self.brand_mapper.to_dto(obj.brand),
            "created_by": self.user_mapper.to_dto(obj.created_by),
            "created_at": obj.created_at,
            "is_private": obj.is_private,
            "image_url": obj.image_url
        }

    def to_object(self, dto: dict, not_update: bool = False) -> Optional[Product]:
        if not dto:
            return None

        product = None
        found = False
        if dto.get("id"):
            product = self.product_dao.find_by_id(dto.get("id"), AuthenticationContext.get_current_user())
            found = product is not None

        if not found:
            product = Product()
            product.id = dto.get("id")
            product.created_at = dto.get("created_at")
            product.created_by = self.user_mapper.to_object(dto.get("created_by"), not_update=True)
            product.is_private = dto.get("is_private")

        if not found or not not_update:
            product.name = dto.get("name")
            product.image_url = dto.get("image_url")
            product.brand = self.brand_mapper.to_object(dto.get("brand"), not_update=True)
            product.product_type = self.product_type_mapper.to_object(dto.get("product_type"), not_update=True)

        return product

    def get_required_fields_to_insert(self):
        return ["name"]

    def get_required_fields_to_update(self):
        return ["id", "name"]

    def get_entity_name(self):
        return Product.__name__
