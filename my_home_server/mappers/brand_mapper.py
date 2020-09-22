from typing import Optional

from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.mappers.user_mapper import UserMapper
from my_home_server.models.brand import Brand


class BrandMapper(MapperInterface):

    def __init__(self):
        self.user_mapper = UserMapper()

    def to_object(self, dto: dict, loaded_object: Brand = None) -> Optional[Brand]:
        if not dto:
            return None

        brand = loaded_object if loaded_object else Brand()
        brand.id = dto.get("id")
        brand.name = dto.get("name")
        brand.is_private = dto.get("is_private")

        if not loaded_object:
            brand.created_at = dto.get("created_at")
            brand.created_by = self.user_mapper.to_object(dto.get("created_by")) \
                if not loaded_object else loaded_object.created_by

        return brand

    def validate_dto(self, dto: dict):
        self.generic_validate_dto(dto, ["name"], Brand.__name__)

    def to_dto(self, brand: Brand) -> Optional[dict]:
        if not brand:
            return None

        return {
            "id": brand.id,
            "name": brand.name,
            "is_private": brand.is_private,
            "created_by": {},
            "created_at": brand.created_at
        }
