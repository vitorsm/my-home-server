from typing import List, Optional

from my_home_server.exceptions.invalid_dto_exception import InvalidDTOException
from my_home_server.exceptions.no_mapper import NoMapper
from my_home_server.mappers.brand_mapper import BrandMapper
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.mappers.product_mapper import ProductMapper
from my_home_server.mappers.product_type_mapper import ProductTypeMapper
from my_home_server.mappers.purchase_list_mapper import PurchaseListMapper
from my_home_server.mappers.purchase_mapper import PurchaseMapper
from my_home_server.mappers.user_group_mapper import UserGroupMapper
from my_home_server.mappers.user_mapper import UserMapper
from my_home_server.models.brand import Brand
from my_home_server.models.product import Product
from my_home_server.models.product_type import ProductType
from my_home_server.models.purchase import Purchase
from my_home_server.models.purchase_list import PurchaseList
from my_home_server.models.user import User
from my_home_server.models.user_group import UserGroup


class Mapper(object):

    mappers = {
        Brand.__name__:  BrandMapper(),
        User.__name__: UserMapper(),
        ProductType.__name__: ProductTypeMapper(),
        Product.__name__: ProductMapper(),
        PurchaseList.__name__: PurchaseListMapper(),
        Purchase.__name__: PurchaseMapper(),
        UserGroup.__name__: UserGroupMapper()
    }

    @staticmethod
    def get_mapper(entity_name: str) -> MapperInterface:
        mapper = Mapper.mappers.get(entity_name)

        if not mapper:
            raise NoMapper(entity_name)

        return mapper

    @staticmethod
    def map_to_dto(obj) -> Optional[dict]:
        if not obj:
            return None

        return Mapper.get_mapper(type(obj).__name__).to_dto(obj)

    @staticmethod
    def map_to_dto_from_list(obj: list) -> Optional[list]:
        if not obj:
            return None

        return [Mapper.get_mapper(type(item).__name__).to_dto(item) for item in obj]

    @staticmethod
    def map_to_obj(dto: dict, entity_name: str) -> Optional[object]:
        if not dto:
            return None

        return Mapper.get_mapper(entity_name).to_object(dto)

    @staticmethod
    def map_to_obj_from_list(dto_list: List[dict], entity_name: str) -> Optional[object]:
        if not dto_list:
            return None

        return [Mapper.get_mapper(entity_name).to_object(dto) for dto in dto_list]

    @staticmethod
    def validate_dto(dto: dict, required_fields: List[str], entity_name: str):
        if not dto:
            raise InvalidDTOException(entity_name, None)

        if required_fields:
            invalid_fields = list()

            for field_name, value in dto.items():
                if field_name in required_fields and not value:
                    invalid_fields.append(field_name)

            if len(invalid_fields):
                raise InvalidDTOException(entity_name, invalid_fields)
