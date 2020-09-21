from datetime import datetime
from typing import Optional

from my_home_server.dao.product_type_dao import ProductTypeDAO
from my_home_server.exceptions.object_not_found import ObjectNotFoundException
from my_home_server.mappers.mapper import Mapper
from my_home_server.models.product_type import ProductType
from my_home_server.security.authentication_context import AuthenticationContext


class ProductTypeService(object):
    product_type_dao: ProductTypeDAO

    def __init__(self):
        self.mapper = Mapper.get_mapper(ProductType.__name__)

    def create_by_dto(self, dto: dict):
        self.mapper.validate_dto(dto)

        product_type = self.mapper.to_object(dto)
        product_type.created_at = datetime.utcnow()
        product_type.created_by = AuthenticationContext.get_current_user()

        self.product_type_dao.add(product_type)

        return product_type

    def update_by_dto(self, dto: dict):
        self.mapper.validate_dto(dto)

        product_type = self.product_type_dao.find_by_id(dto.get("id"), AuthenticationContext.get_current_user())

        if not product_type:
            raise ObjectNotFoundException(ProductType.__name__, {"id": dto.get("id")})

        product_type = self.mapper.to_object(dto, product_type)
        product_type.parent_product_type = self.find_or_create(dto.get("parent_product_type")) \
            if dto.get("parent_product_type") else None

        self.product_type_dao.commit()

    def delete_by_id(self, product_type_id: int):
        product_type = self.find_by_id(product_type_id)

        if not product_type:
            raise ObjectNotFoundException(ProductType.__name__, {"id": product_type_id})

        self.product_type_dao.delete(product_type)

    def find_or_create(self, dto: dict) -> Optional[ProductType]:
        if not dto or dto.get("id"):
            return None

        product_type = self.find_by_id(dto.get("id"))

        if not product_type:
            product_type = self.create_by_dto(dto)

        return product_type

    def find_by_id(self, product_type_id: int):
        return self.product_type_dao.find_by_id(product_type_id, AuthenticationContext.get_current_user())
