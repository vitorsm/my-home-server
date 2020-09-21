from my_home_server.mappers.mapper import Mapper
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.models.brand import Brand
from my_home_server.models.user import User


class BrandMapper(MapperInterface):
    
    def to_object(self, dto: dict, loaded_object: Brand = None) -> Brand:
        brand = loaded_object if loaded_object else Brand()
        brand.id = dto.get("id")
        brand.name = dto.get("name")
        brand.is_private = dto.get("is_private")

        if not loaded_object:
            brand.created_at = dto.get("created_at")
            brand.created_by = Mapper.map_to_obj(dto.get("created_by"), User.__name__) \
                if not loaded_object else loaded_object.created_by

        return brand

    def validate_dto(self, dto: dict):
        Mapper.validate_dto(dto, ["name"], Brand.__name__)

    def to_dto(self, brand: Brand) -> dict:
        return {
            "id": brand.id,
            "name": brand.name,
            "is_private": brand.is_private,
            "created_by": {},
            "created_at": brand.created_at
        }
