from datetime import datetime

from my_home_server.dao.purchase_list_dao import PurchaseListDAO
from my_home_server.mappers.mapper import Mapper
from my_home_server.models.purchase_list import PurchaseList
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.services.product_service import ProductService


class PurchaseListService(object):
    def __init__(self, purchase_list_dao: PurchaseListDAO, product_service: ProductService):
        self.purchase_list_dao = purchase_list_dao
        self.product_service = product_service
        self.mapper = Mapper.get_mapper(PurchaseList.__name__)

    def create_purchase_list(self, dto: dict):
        self.mapper.validate_dto(dto)

        purchase_list = self.mapper.to_object(dto)
        purchase_list.created_at = datetime.utcnow()
        purchase_list.created_by = AuthenticationContext.get_current_user()

        self.purchase_list_dao.add(purchase_list)

        return purchase_list

    def update_purchase_list(self, dto: dict):
        self.mapper.validate_dto(dto)

        
