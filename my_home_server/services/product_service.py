from datetime import datetime

from my_home_server.dao.product_dao import ProductDAO
from my_home_server.exceptions.object_not_found import ObjectNotFoundException
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

    def create_by_dto(self, dto: dict):
        self.mapper.validate_dto_to_insert(dto)

        product = self.mapper.to_object(dto)
        product.created_at = datetime.utcnow()
        product.created_by = AuthenticationContext.get_current_user()

        brand = self.brand_service.find_or_create(dto.get("brand"))
        product_type = self.product_type_service.find_or_create(dto.get("product_type"))

        product.brand = brand
        product.product_type = product_type

        self.product_dao.add(product)

        return product

    def update_by_dto(self, dto: dict):
        self.mapper.validate_dto_to_update(dto)

        product = self.product_dao.find_by_id(dto.get("id"), AuthenticationContext.get_current_user())

        if not product:
            raise ObjectNotFoundException(Product.__name__, {"id": dto.get("id")})

        product = self.mapper.to_object(dto, product)

        if product.brand and product.brand.id:
            self.product_dao.expunge(product.brand)
        if product.product_type and product.product_type.id:
            self.product_dao.expunge(product.product_type)

        brand = self.brand_service.find_or_create(dto.get("brand"))
        product_type = self.product_type_service.find_or_create(dto.get("product_type"))

        product.brand = brand
        product.product_type = product_type

        self.product_dao.commit()

    def delete_by_id(self, product_id: int):
        product = self.product_dao.find_by_id(product_id, AuthenticationContext.get_current_user())

        if not product:
            raise ObjectNotFoundException(Product.__name__, {"id": product_id})

        self.product_dao.delete(product)

    def find_by_id(self, product_id: int) -> Product:
        return self.product_dao.find_by_id(product_id, AuthenticationContext.get_current_user())

    def find_or_create(self, dto: dict) -> Product:
        if not dto.get("id"):
            return None

        product = self.product_dao.find_by_id(dto.get("id"), AuthenticationContext.get_current_user())

        if not product:
            product = self.create_by_dto(dto)

        return product
