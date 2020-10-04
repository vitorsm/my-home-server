from datetime import datetime
from typing import List, Optional

from my_home_server.dao.product_dao import ProductDAO
from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.exceptions.object_not_found_exception import ObjectNotFoundException
from my_home_server.mappers.product_mapper import ProductMapper
from my_home_server.models.product import Product
from my_home_server.models.product_type import ProductType
from my_home_server.models.user import User
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.services.brand_service import BrandService
from my_home_server.services.product_type_service import ProductTypeService
from my_home_server.utils.sql_utils import transaction


class ProductService(object):
    def __init__(self, product_dao: ProductDAO, brand_service: BrandService, product_type_service: ProductTypeService,
                 product_mapper: ProductMapper):
        self.product_dao = product_dao
        self.brand_service = brand_service
        self.product_type_service = product_type_service
        self.mapper = product_mapper

    @transaction
    def create(self, product: Product):
        ProductService.fill_to_create(product, datetime.utcnow(), AuthenticationContext.get_current_user())

        self.product_dao.add(product)

        return product

    @transaction
    def create_from_dto(self, dto: dict):
        self.mapper.validate_dto_to_insert(dto)
        product = self.mapper.to_object(dto)

        return self.create(product)

    @transaction
    def update_from_dto(self, dto: dict):
        self.mapper.validate_dto_to_update(dto)

        product = self.product_dao.find_by_id(dto.get("id"), AuthenticationContext.get_current_user())

        if not product:
            raise ObjectNotFoundException(ErrorCode.PRODUCT_TO_UPDATE_NOT_FOUND,
                                          Product.__name__, {"id": dto.get("id")})

        product = self.mapper.to_object(dto)
        ProductService.fill_to_create(product, datetime.utcnow(), AuthenticationContext.get_current_user())

        self.product_dao.update(product)

        return product

    @transaction
    def delete_by_id(self, product_id: int):
        product = self.product_dao.find_by_id(product_id, AuthenticationContext.get_current_user())

        if not product:
            raise ObjectNotFoundException(ErrorCode.PRODUCT_TO_DELETE_NOT_FOUND, Product.__name__, {"id": product_id})

        self.product_dao.delete(product)

    def find_by_id(self, product_id: int) -> Product:
        return self.product_dao.find_by_id(product_id, AuthenticationContext.get_current_user())

    def find_all(self) -> List[Product]:
        return self.product_dao.find_all(AuthenticationContext.get_current_user())

    def find_or_create_from_dto(self, dto: dict) -> Optional[Product]:
        if not dto.get("id"):
            return None

        product = self.product_dao.find_by_id(dto.get("id"), AuthenticationContext.get_current_user())

        if not product:
            product = self.create_from_dto(dto)

        return product

    @staticmethod
    def fill_to_create(product: Product, create_at: datetime, created_by: User):
        if not product:
            return

        if not product.created_by:
            product.created_at = create_at
            product.created_by = created_by
            product.is_private = True

        ProductTypeService.fill_to_create(product.product_type, create_at, created_by)
        BrandService.fill_to_create(product.brand, create_at, created_by)

    def commit(self):
        self.product_dao.commit()
