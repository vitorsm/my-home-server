from typing import List, Optional

from my_home_server.dao.purchase_list_dao import PurchaseListDAO
from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.mappers.product_mapper import ProductMapper
from my_home_server.mappers.user_mapper import UserMapper
from my_home_server.models.purchase_list_product import PurchaseListProduct
from my_home_server.models.purchase_list import PurchaseList
from my_home_server.security.authentication_context import AuthenticationContext


class PurchaseListMapper(MapperInterface):
    def __init__(self, purchase_list_dao: PurchaseListDAO, user_mapper: UserMapper, product_mapper: ProductMapper):
        self.user_mapper = user_mapper
        self.product_mapper = product_mapper
        self.purchase_list_dao = purchase_list_dao

    def get_error_code_when_dto_invalid_to_insert(self):
        return ErrorCode.INVALID_INPUT_CREATE_PURCHASE_LIST

    def get_error_code_when_dto_invalid_to_update(self):
        return ErrorCode.INVALID_INPUT_UPDATE_PURCHASE_LIST

    def to_dto(self, obj: PurchaseList) -> Optional[dict]:
        if not obj:
            return None

        return {
            "id": obj.id,
            "name": obj.name,
            "created_at": obj.created_at,
            "created_by": self.user_mapper.to_dto(obj.created_by),
            "products": self.__products_to_dto(obj.purchase_products)
        }

    def to_object(self, dto: dict, not_update: bool = False) -> Optional[PurchaseList]:
        if not dto:
            return None

        purchase_list = None
        found = False
        if dto.get("id"):
            purchase_list = self.purchase_list_dao.find_by_id(dto.get("id"), AuthenticationContext.get_current_user())
            found = purchase_list is not None

        if not found:
            purchase_list = PurchaseList()
            purchase_list.id = dto.get("id")
            purchase_list.created_by = self.user_mapper.to_object(dto.get("created_by"), not_update=True)
            purchase_list.created_at = dto.get("created_at")

        if not found or not not_update:
            purchase_list.name = dto.get("name")
            self.__products_to_obj(dto.get("products"), purchase_list)

        return purchase_list

    def get_required_fields_to_insert(self):
        return ["name"]

    def get_required_fields_to_update(self):
        return ["id", "name"]

    def get_entity_name(self):
        return PurchaseList.__name__

    def __products_to_obj(self, purchase_products_dto: List[dict], purchase_list: PurchaseList):

        if not purchase_products_dto:
            purchase_list.products = list()
            return

        if purchase_list.purchase_products:
            dto_ids = [p.get("id") for p in purchase_products_dto]

            purchase_list.purchase_products[:] = [p for p in purchase_list.purchase_products
                                                  if p.product.id in dto_ids]

        for dto in purchase_products_dto:
            purchase_product = next((p for p in purchase_list.purchase_products if p.product.id == dto.get("id")),
                                    None)

            if not purchase_product:
                purchase_product = PurchaseListProduct()
                purchase_product.product = self.product_mapper.to_object(dto, not_update=True)
                purchase_product.purchase_list = purchase_list

            purchase_product.quantity = dto.get("quantity")
            purchase_product.estimated_value = dto.get("value")

    def __products_to_dto(self, purchase_products: List[PurchaseListProduct]) -> List[dict]:
        products = list()

        if purchase_products:
            for purchase_product in purchase_products:
                dto = self.product_mapper.to_dto(purchase_product.product)

                dto.update({
                    "value": purchase_product.estimated_value,
                    "quantity": purchase_product.quantity
                })

                products.append(dto)

        return products
