from datetime import datetime
from typing import Optional

from my_home_server.dao.product_type_dao import ProductTypeDAO
from my_home_server.exceptions.object_not_found import ObjectNotFoundException
from my_home_server.mappers.mapper import Mapper
from my_home_server.models.product_type import ProductType
from my_home_server.models.user import User
from my_home_server.security.authentication_context import AuthenticationContext


class ProductTypeService(object):
    def __init__(self, product_type_dao: ProductTypeDAO):
        self.product_type_dao = product_type_dao
        self.mapper = Mapper.get_mapper(ProductType.__name__)

    def create_by_dto(self, dto: dict):
        self.mapper.validate_dto_to_insert(dto)

        product_type = self.mapper.to_object(dto)
        created_at = datetime.utcnow()

        product_type.created_at = created_at
        product_type.created_by = AuthenticationContext.get_current_user()

        self.__fill_parent_product_type_to_save(product_type, AuthenticationContext.get_current_user(), created_at,
                                                is_update=False)

        self.product_type_dao.add(product_type)

        return product_type

    def __fill_parent_product_type_to_save(self, product_type: ProductType, created_by: User, created_at: datetime,
                                           is_update: bool):
        if product_type.parent_product_type:
            if product_type.parent_product_type.id:
                parent_id = product_type.parent_product_type.id
                if is_update:
                    self.product_type_dao.expunge(product_type.parent_product_type)
                    product_type.parent_product_type = None
                product_type.parent_product_type = self.find_by_id(parent_id)

            else:
                product_type.parent_product_type.created_by = created_by
                product_type.parent_product_type.created_at = created_at
                self.__fill_parent_product_type_to_save(product_type.parent_product_type, created_by, created_at,
                                                        is_update)

    def update_by_dto(self, dto: dict):
        self.mapper.validate_dto_to_update(dto)

        product_type = self.product_type_dao.find_by_id(dto.get("id"), AuthenticationContext.get_current_user())

        if not product_type:
            raise ObjectNotFoundException(ProductType.__name__, {"id": dto.get("id")})

        product_type = self.mapper.to_object(dto, product_type)

        self.__fill_parent_product_type_to_save(product_type, AuthenticationContext.get_current_user(),
                                                datetime.utcnow(), is_update=True)

        self.product_type_dao.commit()

        return product_type

    def delete_by_id(self, product_type_id: int):
        product_type = self.find_by_id(product_type_id)

        if not product_type:
            raise ObjectNotFoundException(ProductType.__name__, {"id": product_type_id})

        self.product_type_dao.delete(product_type)

    def find_or_create(self, dto: dict) -> Optional[ProductType]:
        if not dto or not dto.get("id"):
            return None

        product_type = self.find_by_id(dto.get("id"))

        if not product_type:
            product_type = self.create_by_dto(dto)

        return product_type

    def find_by_id(self, product_type_id: int):
        return self.product_type_dao.find_by_id(product_type_id, AuthenticationContext.get_current_user())

    def find_all(self):
        return self.product_type_dao.find_allowed(AuthenticationContext.get_current_user())
