from my_home_server.mappers.mapper import Mapper
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.models.product_type import ProductType
from my_home_server.models.user import User


class ProductTypeMapper(MapperInterface):
    def to_dto(self, obj: ProductType) -> dict:
        return {
            "id": obj.id,
            "name": obj.name,
            "description": obj.description,
            "parent_product_type": self.to_dto(obj.parent_product_type) if obj.parent_product_type else None,
            "is_private": obj.is_private,
            "created_by": Mapper.map_to_dto(obj.created_by),
            "created_at": obj.created_at
        }

    def to_object(self, dto: dict) -> object:
        product_type = ProductType()
        product_type.id = dto.get("id")
        product_type.name = dto.get("name")
        product_type.parent_product_type = self.to_object(dto.get("parent_product_type")) \
            if dto.get("parent_product_type") else None
        product_type.created_by = Mapper.map_to_obj(dto.get("created_by"), User.__name__)
        product_type.is_private = dto.get("is_private")
        product_type.description = dto.get("description")
        product_type.created_at = dto.get("created_at")

        return product_type

    def validate_dto(self, dto: dict):
        Mapper.validate_dto(dto, ["name"], ProductType.__name__)
