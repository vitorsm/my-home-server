from typing import List, Optional

from my_home_server.dao.purchase_dao import PurchaseDAO
from my_home_server.exceptions.error_code import ErrorCode
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.mappers.product_mapper import ProductMapper
from my_home_server.mappers.purchase_list_mapper import PurchaseListMapper
from my_home_server.mappers.user_mapper import UserMapper
from my_home_server.models.purchase import Purchase
from my_home_server.models.purchase_product import PurchaseProduct
from my_home_server.security.authentication_context import AuthenticationContext


class PurchaseMapper(MapperInterface):
    def __init__(self, purchase_dao: PurchaseDAO, user_mapper: UserMapper, product_mapper: ProductMapper,
                 purchase_list_mapper: PurchaseListMapper):
        self.purchase_dao = purchase_dao
        self.user_mapper = user_mapper
        self.product_mapper = product_mapper
        self.purchase_list_mapper = purchase_list_mapper

    def get_error_code_when_dto_invalid_to_insert(self):
        return ErrorCode.INVALID_INPUT_CREATE_PURCHASE

    def get_error_code_when_dto_invalid_to_update(self):
        return ErrorCode.INVALID_INPUT_UPDATE_PURCHASE

    def to_dto(self, obj: Purchase) -> Optional[dict]:
        if not obj:
            return None

        return {
            "id": obj.id,
            "name": obj.name,
            "created_at": obj.created_at,
            "created_by": self.user_mapper.to_dto(obj.created_by),
            "purchase_list": self.purchase_list_mapper.to_dto(obj.purchase_list),
            "products": self.__products_to_dto(obj.products)
        }

    def to_object(self, dto: dict, not_update: bool = False) -> Optional[Purchase]:
        if dto is None:
            return None

        purchase = None
        found = False
        if dto.get("id"):
            purchase = self.purchase_dao.find_by_id(dto.get("id"), AuthenticationContext.get_current_user())
            found = purchase is not None

        if not found:
            purchase = Purchase()
            purchase.id = dto.get("id")
            purchase.created_at = dto.get("created_at")
            purchase.created_by = self.user_mapper.to_object(dto.get("created_by"), not_update=True)

        if not found or not not_update:
            purchase.name = dto.get("name")
            purchase.purchase_list = self.purchase_list_mapper.to_object(dto.get("purchase_list"), not_update=True)
            self.__products_to_obj(dto.get("products"), purchase)

        return purchase

    def get_required_fields_to_insert(self):
        return []

    def get_required_fields_to_update(self):
        return ["id"]

    def get_entity_name(self):
        return Purchase.__name__

    def __products_to_obj(self, purchase_products_dto: List[dict], purchase: Purchase):
        if not purchase_products_dto:
            purchase.products = list()
            return

        if purchase.products:
            dto_ids = [p.get("id") for p in purchase_products_dto]
            purchase.products[:] = [p for p in purchase.products if p.product.id in dto_ids]

        for dto in purchase_products_dto:
            purchase_product = next((p for p in purchase.products if p.product.id == dto.get("id")), None)
            if not purchase_product:
                purchase_product = PurchaseProduct()
                purchase_product.product = self.product_mapper.to_object(dto, not_update=True)
                purchase_product.purchase = purchase
                purchase.products.append(purchase_product)

            purchase_product.quantity = dto.get("quantity")
            purchase_product.value = dto.get("value")

    def __products_to_dto(self, purchase_products: List[PurchaseProduct]) -> List[dict]:
        if not purchase_products:
            return list()

        products = list()
        for purchase_product in purchase_products:
            dto = self.product_mapper.to_dto(purchase_product.product)
            dto.update({
                "value": purchase_product.value,
                "quantity": purchase_product.quantity
            })

            products.append(dto)

        return products
