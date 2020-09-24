from datetime import datetime
from typing import Optional, List

from my_home_server.dao.purchase_dao import PurchaseDAO
from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.exceptions.object_not_found_exception import ObjectNotFoundException
from my_home_server.mappers.mapper import Mapper
from my_home_server.models.purchase import Purchase
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.services.product_service import ProductService
from my_home_server.services.purchase_list_service import PurchaseListService
from my_home_server.utils.sql_utils import transaction


class PurchaseService(object):
    def __init__(self, purchase_dao: PurchaseDAO, purchase_list_service: PurchaseListService,
                 product_service: ProductService):
        self.purchase_dao = purchase_dao
        self.purchase_list_service = purchase_list_service
        self.product_service = product_service
        self.mapper = Mapper.get_mapper(Purchase.__name__)

    def find_by_id(self, purchase_id: int) -> Optional[Purchase]:
        return self.purchase_dao.find_by_id(purchase_id, AuthenticationContext.get_current_user())

    @transaction
    def create(self, purchase: Purchase) -> Purchase:
        purchase.id = None

        purchase.created_by = AuthenticationContext.get_current_user()
        purchase.created_at = datetime.utcnow()

        if purchase.purchase_list:
            self.purchase_dao.expunge(purchase.purchase_list)
            purchase.purchase_list = self.purchase_list_service.find_by_id(purchase.purchase_list.id)

        self.__fill_purchase_products(purchase)

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

        purchase = self.mapper.to_object(dto, purchase)

        if purchase.purchase_list:
            self.purchase_dao.expunge(purchase.purchase_list)
            purchase.purchase_list = self.purchase_list_service.find_by_id(purchase.purchase_list.id)

        self.__fill_purchase_products(purchase)

        self.purchase_dao.update(purchase)

    @transaction
    def delete_by_id(self, purchase_id: int):
        purchase = self.find_by_id(purchase_id)

        if not purchase:
            raise ObjectNotFoundException(ErrorCode.PURCHASE_TO_DELETE_NOT_FOUND,
                                          Purchase.__name__, {"id": purchase_id})

        self.purchase_dao.delete(purchase)

    def __fill_purchase_products(self, purchase: Purchase):
        if not purchase.products or not len(purchase.products):
            return

        for purchase_product in purchase.products:
            purchase_product.product = self.product_service.fetch_or_create(purchase_product.product)

    def find_all(self) -> List[Purchase]:
        return self.purchase_dao.find_all_by_user(AuthenticationContext.get_current_user())

    def commit(self):
        self.purchase_dao.commit()
