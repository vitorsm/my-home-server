from datetime import datetime
from typing import Optional

from my_home_server.dao.product_type_dao import ProductTypeDAO
from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.exceptions.object_not_found_exception import ObjectNotFoundException
from my_home_server.mappers.product_type_mapper import ProductTypeMapper
from my_home_server.models.product_type import ProductType
from my_home_server.models.user import User
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.utils.sql_utils import transaction


class ProductTypeService(object):
    def __init__(self, product_type_dao: ProductTypeDAO, product_type_mapper: ProductTypeMapper):
        self.product_type_dao = product_type_dao
        self.mapper = product_type_mapper

    @transaction
    def create(self, product_type: ProductType):
        ProductTypeService.fill_to_create(product_type, datetime.utcnow(), AuthenticationContext.get_current_user())

        self.product_type_dao.add(product_type)

        return product_type

    @transaction
    def create_from_dto(self, dto: dict):
        self.mapper.validate_dto_to_insert(dto)
        product_type = self.mapper.to_object(dto)

        return self.create(product_type)

    @transaction
    def update_from_dto(self, dto: dict):
        self.mapper.validate_dto_to_update(dto)

        product_type = self.product_type_dao.find_by_id(dto.get("id"), AuthenticationContext.get_current_user())

        if not product_type:
            raise ObjectNotFoundException(ErrorCode.PRODUCT_TYPE_TO_UPDATE_NOT_FOUND,
                                          ProductType.__name__, {"id": dto.get("id")})

        product_type = self.mapper.to_object(dto)
        ProductTypeService.fill_to_create(product_type, datetime.utcnow(), AuthenticationContext.get_current_user())

        self.product_type_dao.commit()

        return product_type

    @transaction
    def delete_by_id(self, product_type_id: int):
        product_type = self.find_by_id(product_type_id)

        if not product_type:
            raise ObjectNotFoundException(ErrorCode.PRODUCT_TYPE_TO_DELETE_NOT_FOUND, ProductType.__name__, {"id": product_type_id})

        self.product_type_dao.delete(product_type)

    def find_or_create_from_dto(self, dto: dict) -> Optional[ProductType]:
        if not dto or not dto.get("id"):
            return None

        product_type = self.find_by_id(dto.get("id"))

        if not product_type:
            product_type = self.create_from_dto(dto)

        return product_type

    def find_by_id(self, product_type_id: int):
        return self.product_type_dao.find_by_id(product_type_id, AuthenticationContext.get_current_user())

    def find_all(self):
        return self.product_type_dao.find_allowed(AuthenticationContext.get_current_user())

    @staticmethod
    def fill_to_create(product_type: ProductType, created_at: datetime, created_by: User):
        if not product_type:
            return

        if not product_type.created_by:
            product_type.created_by = created_by
            product_type.created_at = created_at
            product_type.is_private = True

        if product_type.parent_product_type:
            ProductTypeService.fill_to_create(product_type.parent_product_type, created_at, created_by)

    def commit(self):
        self.product_type_dao.commit()
