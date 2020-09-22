from typing import Optional

from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.mappers.user_mapper import UserMapper
from my_home_server.models.product_type import ProductType


class ProductTypeMapper(MapperInterface):

    def __init__(self):
        self.user_mapper = UserMapper()

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

    def to_object(self, dto: dict, loaded_object: ProductType = None) -> Optional[object]:
        if not dto:
            return None

        product_type = loaded_object if loaded_object else ProductType()
        product_type.id = dto.get("id")
        product_type.name = dto.get("name")
        product_type.parent_product_type = self.to_object(dto.get("parent_product_type")) \
            if dto.get("parent_product_type") else None
        product_type.is_private = dto.get("is_private")
        product_type.description = dto.get("description")

        if not loaded_object:
            product_type.created_by = self.user_mapper.to_object(dto.get("created_by"))
            product_type.created_at = dto.get("created_at")

        return product_type

    def get_required_fields_to_insert(self):
        return ["name"]

    def get_required_fields_to_update(self):
        return ["id", "name"]

    def get_entity_name(self):
        return ProductType.__name__
