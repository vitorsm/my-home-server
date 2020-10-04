from datetime import datetime
from functools import wraps
from typing import Optional, List

from my_home_server.dao.purchase_list_dao import PurchaseListDAO
from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.exceptions.object_not_found_exception import ObjectNotFoundException

from my_home_server.mappers.purchase_list_mapper import PurchaseListMapper
from my_home_server.models.purchase_list import PurchaseList
from my_home_server.models.user import User
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.services.product_service import ProductService
from my_home_server.utils.sql_utils import transaction


class PurchaseListService(object):
    def __init__(self, purchase_list_dao: PurchaseListDAO, product_service: ProductService,
                 purchase_list_mapper: PurchaseListMapper):
        self.purchase_list_dao = purchase_list_dao
        self.product_service = product_service
        self.mapper = purchase_list_mapper

    def find_by_id(self, purchase_list_id: int) -> Optional[PurchaseList]:
        return self.purchase_list_dao.find_by_id(purchase_list_id, AuthenticationContext.get_current_user())

    def find_all(self) -> List[PurchaseList]:
        return self.purchase_list_dao.find_all_by_user(AuthenticationContext.get_current_user())

    @transaction
    def create_from_dto(self, dto: dict):
        self.mapper.validate_dto_to_insert(dto)

        purchase_list = self.mapper.to_object(dto)

        PurchaseListService.fill_to_create(purchase_list, datetime.utcnow(), AuthenticationContext.get_current_user())
        self.purchase_list_dao.add(purchase_list)

        return purchase_list

    @transaction
    def update_from_dto(self, dto: dict):
        self.mapper.validate_dto_to_update(dto)

        purchase_list = self.find_by_id(dto.get("id"))

        if not purchase_list:
            raise ObjectNotFoundException(ErrorCode.PURCHASE_LIST_TO_UPDATE_NOT_FOUND,
                                          PurchaseList.__name__, {"id": dto.get("id")})

        self.mapper.to_object(dto)

        PurchaseListService.fill_to_create(purchase_list, datetime.utcnow(), AuthenticationContext.get_current_user())

        self.purchase_list_dao.update(purchase_list)

        return purchase_list

    @transaction
    def delete_by_id(self, purchase_list_id: int):
        purchase_list = self.find_by_id(purchase_list_id)

        if not purchase_list:
            raise ObjectNotFoundException(ErrorCode.PURCHASE_LIST_TO_DELETE_NOT_FOUND,
                                          PurchaseList.__name__, {"id": purchase_list_id})

        self.purchase_list_dao.delete(purchase_list)

    @staticmethod
    def fill_to_create(purchase_list: PurchaseList, created_at: datetime, created_by: User):
        if not purchase_list:
            return

        if not purchase_list.created_by:
            purchase_list.created_by = created_by
            purchase_list.created_at = created_at

        if not purchase_list.purchase_products:
            return

        for purchase_product in purchase_list.purchase_products:
            ProductService.fill_to_create(purchase_product.product, created_at, created_by)

    def commit(self):
        self.purchase_list_dao.commit()
