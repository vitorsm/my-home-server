from datetime import datetime
from typing import Optional

from my_home_server.dao.purchase_list_dao import PurchaseListDAO
from my_home_server.exceptions.object_not_found import ObjectNotFoundException
from my_home_server.mappers.mapper import Mapper
from my_home_server.models.purchase_list import PurchaseList
from my_home_server.security.authentication_context import AuthenticationContext
from my_home_server.services.product_service import ProductService


class PurchaseListService(object):
    def __init__(self, purchase_list_dao: PurchaseListDAO, product_service: ProductService):
        self.purchase_list_dao = purchase_list_dao
        self.product_service = product_service
        self.mapper = Mapper.get_mapper(PurchaseList.__name__)

    def find_by_id(self, purchase_list_id: int) -> Optional[PurchaseList]:
        return self.purchase_list_dao.find_by_id(purchase_list_id, AuthenticationContext.get_current_user())

    def create_by_dto(self, dto: dict):
        self.mapper.validate_dto(dto)

        purchase_list = self.mapper.to_object(dto)
        purchase_list.created_at = datetime.utcnow()
        purchase_list.created_by = AuthenticationContext.get_current_user()

        self.purchase_list_dao.add(purchase_list)

        return purchase_list

    def update_by_dto(self, dto: dict):
        self.mapper.validate_dto(dto)

        purchase_list = self.find_by_id(dto.get("id"))

        if not purchase_list:
            raise ObjectNotFoundException(PurchaseList.__name__, {"id": dto.get("id")})

        self.mapper.to_object(dto, purchase_list)

        self.purchase_list_dao.commit()

    def delete_by_id(self, purchase_list_id: int):
        purchase_list = self.find_by_id(purchase_list_id)

        if not purchase_list:
            raise ObjectNotFoundException(PurchaseList.__name__, {"id": purchase_list_id})

        self.purchase_list_dao.delete(purchase_list)
