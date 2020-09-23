from datetime import datetime
from functools import wraps
from typing import Optional, List

from my_home_server.dao.purchase_list_dao import PurchaseListDAO
from my_home_server.exceptions.object_not_found import ObjectNotFoundException
from my_home_server.mappers.mapper import Mapper
from my_home_server.models.purchase_list import PurchaseList
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.services.product_service import ProductService
from my_home_server.utils.sql_utils import transaction


class PurchaseListService(object):
    def __init__(self, purchase_list_dao: PurchaseListDAO, product_service: ProductService):
        self.purchase_list_dao = purchase_list_dao
        self.product_service = product_service
        self.mapper = Mapper.get_mapper(PurchaseList.__name__)

    def find_by_id(self, purchase_list_id: int) -> Optional[PurchaseList]:
        return self.purchase_list_dao.find_by_id(purchase_list_id, AuthenticationContext.get_current_user())

    def find_all(self) -> List[PurchaseList]:
        return self.purchase_list_dao.find_all_by_user(AuthenticationContext.get_current_user())

    @transaction
    def create_from_dto(self, dto: dict):
        self.mapper.validate_dto_to_insert(dto)

        purchase_list = self.mapper.to_object(dto)
        created_at = datetime.utcnow()
        purchase_list.created_at = created_at
        purchase_list.created_by = AuthenticationContext.get_current_user()

        self.__fill_purchase_list_products(purchase_list)
        self.purchase_list_dao.add(purchase_list)

        return purchase_list

    def __fill_purchase_list_products(self, purchase_list: PurchaseList):
        if not purchase_list.purchase_products or not len(purchase_list.purchase_products):
            return

        for product_purchase in purchase_list.purchase_products:
            product_purchase.product = self.product_service.fetch_or_create(product_purchase.product)

    @transaction
    def update_from_dto(self, dto: dict):
        self.mapper.validate_dto_to_update(dto)

        purchase_list = self.find_by_id(dto.get("id"))

        if not purchase_list:
            raise ObjectNotFoundException(PurchaseList.__name__, {"id": dto.get("id")})

        self.mapper.to_object(dto, purchase_list)

        self.__fill_purchase_list_products(purchase_list)

        self.purchase_list_dao.update(purchase_list)

    @transaction
    def delete_by_id(self, purchase_list_id: int):
        purchase_list = self.find_by_id(purchase_list_id)

        if not purchase_list:
            raise ObjectNotFoundException(PurchaseList.__name__, {"id": purchase_list_id})

        self.purchase_list_dao.delete(purchase_list)

    def commit(self):
        self.purchase_list_dao.commit()
