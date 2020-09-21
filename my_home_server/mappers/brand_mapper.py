from my_home_server.mappers.mapper import Mapper
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.models.brand import Brand


class BrandMapper(MapperInterface):

    def to_object(self, dto: dict) -> Brand:
        brand = Brand()
        brand.id = dto.get("id")
        brand.name = dto.get("name")
        brand.created_at = dto.get("created_at")
        brand.is_private = dto.get("is_private")
        brand.created_by = Mapper.mappers

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
