from datetime import datetime
from typing import Optional, List

from my_home_server.dao.purchase_dao import PurchaseDAO
from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.exceptions.object_not_found_exception import ObjectNotFoundException

from my_home_server.mappers.purchase_mapper import PurchaseMapper
from my_home_server.models.purchase import Purchase
from my_home_server.models.user import User
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.services.product_service import ProductService
from my_home_server.services.purchase_list_service import PurchaseListService
from my_home_server.utils.sql_utils import transaction


class PurchaseService(object):
    def __init__(self, purchase_dao: PurchaseDAO, purchase_list_service: PurchaseListService,
                 product_service: ProductService, purchase_mapper: PurchaseMapper):
        self.purchase_dao = purchase_dao
        self.purchase_list_service = purchase_list_service
        self.product_service = product_service
        self.mapper = purchase_mapper

    def find_by_id(self, purchase_id: int) -> Optional[Purchase]:
        return self.purchase_dao.find_by_id(purchase_id, AuthenticationContext.get_current_user())

    @transaction
    def create(self, purchase: Purchase) -> Purchase:
        purchase.id = None

        PurchaseService.fill_to_create(purchase, datetime.utcnow(), AuthenticationContext.get_current_user())

        self.purchase_dao.add(purchase)

        return purchase

    @transaction
    def create_from_dto(self, dto: dict):
        self.mapper.validate_dto_to_insert(dto)

        purchase = self.mapper.to_object(dto)
        return self.create(purchase)

    @transaction
    def update_from_dto(self, dto: dict):
        self.mapper.validate_dto_to_update(dto)

        purchase = self.find_by_id(dto.get("id"))

        if not purchase:
            raise ObjectNotFoundException(ErrorCode.PURCHASE_TO_UPDATE_NOT_FOUND,
                                          Purchase.__name__, {"id": dto.get("id")})

        purchase = self.mapper.to_object(dto)

        PurchaseService.fill_to_create(purchase, datetime.utcnow(), AuthenticationContext.get_current_user())

        self.purchase_dao.update(purchase)

        return purchase

    @transaction
    def delete_by_id(self, purchase_id: int):
        purchase = self.find_by_id(purchase_id)

        if not purchase:
            raise ObjectNotFoundException(ErrorCode.PURCHASE_TO_DELETE_NOT_FOUND,
                                          Purchase.__name__, {"id": purchase_id})

        self.purchase_dao.delete(purchase)

    def find_all(self) -> List[Purchase]:
        return self.purchase_dao.find_all_by_user(AuthenticationContext.get_current_user())

    @staticmethod
    def fill_to_create(purchase: Purchase, created_at: datetime, created_by: User):
        if not purchase.created_by:
            purchase.created_by = created_by
            purchase.created_at = created_at

        PurchaseListService.fill_to_create(purchase.purchase_list, created_at, created_by)

        if not purchase.products:
            return

        for purchase_product in purchase.products:
            ProductService.fill_to_create(purchase_product.product, created_at, created_by)

        purchase.fill_total_value()

    def commit(self):
        self.purchase_dao.commit()
