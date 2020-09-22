from typing import Optional

from my_home_server.mappers.brand_mapper import BrandMapper
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.mappers.product_type_mapper import ProductTypeMapper
from my_home_server.mappers.user_mapper import UserMapper
from my_home_server.models.product import Product


class ProductMapper(MapperInterface):
    def __init__(self):
        self.product_type_mapper = ProductTypeMapper()
        self.brand_mapper = BrandMapper()
        self.user_mapper = UserMapper()

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

    def to_object(self, dto: dict, loaded_object: Product = None) -> Optional[Product]:
        if not dto:
            return None

        product = loaded_object if loaded_object else Product()
        product.id = dto.get("id")
        product.name = dto.get("name")
        product.image_url = dto.get("image_url")
        product.is_private = dto.get("is_private")
        product.brand = self.brand_mapper.to_object(dto.get("brand"))
        product.product_type = self.product_type_mapper.to_object(dto.get("product_type"))

        if not loaded_object:
            product.created_at = dto.get("created_at")
            product.created_by = self.user_mapper.to_object(dto.get("created_by"))

        return product

    def validate_dto(self, dto: dict):
        self.generic_validate_dto(dto, ["name"], Product.__name__)
