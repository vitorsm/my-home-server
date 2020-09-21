from my_home_server.mappers.mapper import Mapper
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.models.brand import Brand
from my_home_server.models.product import Product
from my_home_server.models.product_type import ProductType
from my_home_server.models.user import User


class ProductMapper(MapperInterface):
    def to_dto(self, obj: Product) -> dict:
        return {
            "id": obj.id,
            "name": obj.name,
            "product_type": Mapper.map_to_dto(obj.product_type),
            "brand": Mapper.map_to_dto(obj.brand),
            "created_by": Mapper.map_to_dto(obj.created_by),
            "created_at": obj.created_at,
            "is_private": obj.is_private,
            "image_url": obj.image_url
        }

    def to_object(self, dto: dict) -> Product:
        product = Product()
        product.id = dto.get("id")
        product.name = dto.get("name")
        product.image_url = dto.get("image_url")
        product.is_private = dto.get("is_private")
        product.created_at = dto.get("created_at")
        product.created_by = Mapper.map_to_obj(dto.get("created_by"), User.__name__)
        product.brand = Mapper.map_to_obj(dto.get("brand"), Brand.__name__)
        product.product_type = Mapper.map_to_obj(dto.get("product_type"), ProductType.__name__)

        return product

    def validate_dto(self, dto: dict):
        Mapper.validate_dto(dto, ["name"], Product.__name__)
