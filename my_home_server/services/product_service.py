from datetime import datetime

from my_home_server.dao.product_dao import ProductDAO
from my_home_server.mappers.mapper import Mapper
from my_home_server.models.product import Product
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.services.brand_service import BrandService
from my_home_server.services.product_type_service import ProductTypeService


class ProductService(object):
    def __init__(self, product_dao: ProductDAO, brand_service: BrandService, product_type_service: ProductTypeService):
        self.product_dao = product_dao
        self.brand_service = brand_service
        self.product_type_service = product_type_service
        self.mapper = Mapper.get_mapper(Product.__name__)

    def create_product(self, dto: dict):
        self.mapper.validate_dto(dto)

        product = self.mapper.to_object(dto)
        product.created_at = datetime.utcnow()
        product.created_by = AuthenticationContext.get_current_user()

        self.product_dao.add(product)

        return product

    def update_product(self, dto: dict):
        self.mapper.validate_dto(dto)

        product = self.product_dao.find_by_id(dto.get("id"), AuthenticationContext.get_current_user())
        product.name = dto.get("name")
        product.brand = self.brand_service.find_or_create(dto.get("brand"))
        product.created_at = datetime.utcnow()
        product.product_type = self.product_type_service.find_or_create(dto.get("product_type"))

        self.product_dao.commit()

    def find_by_id(self, product_id: int) -> Product:
        return self.product_dao.find_by_id(product_id, AuthenticationContext.get_current_user())
