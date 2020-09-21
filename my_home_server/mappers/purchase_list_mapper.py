from typing import List

from my_home_server.mappers.mapper import Mapper
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.models.purchase_list_product import PurchaseListProduct
from my_home_server.models.purchase_list import PurchaseList
from my_home_server.models.user import User


class PurchaseListMapper(MapperInterface):
    def to_dto(self, obj: PurchaseList) -> dict:
        return {
            "id": obj.id,
            "name": obj.name,
            "created_at": obj.created_at,
            "created_by": Mapper.map_to_dto(obj.created_by),
            "purchase_products": self.__products_to_dto(obj.purchase_products)
        }

    def to_object(self, dto: dict, loaded_object: PurchaseList = None) -> PurchaseList:
        purchase_list = loaded_object if loaded_object else PurchaseList()
        purchase_list.id = dto.get("id")
        purchase_list.name = dto.get("name")
        purchase_list.purchase_products = self.__products_to_obj(dto.get("purchase_products"))

        if not loaded_object:
            purchase_list.created_by = Mapper.map_to_obj(dto.get("created_by"), User.__name__)
            purchase_list.created_at = dto.get("created_at")

        return purchase_list

    def validate_dto(self, dto: dict):
        Mapper.validate_dto(dto, ["name", "purchase_products"], PurchaseList.__name__)

    @staticmethod
    def __products_to_obj(purchase_products_dto: List[dict]) -> List[PurchaseListProduct]:
        products = list()
        for dto in purchase_products_dto:
            purchase_product = PurchaseListProduct()
            purchase_product.product = Mapper.map_to_obj(dto, PurchaseListProduct.__name__)
            purchase_product.quantity = dto.get("quantity")
            purchase_product.value = dto.get("value")
            products.append(purchase_product)

        return products

    @staticmethod
    def __products_to_dto(purchase_products: List[PurchaseListProduct]) -> List[dict]:
        products = list()
        for purchase_product in purchase_products:
            dto = Mapper.map_to_dto(purchase_product.product)
            dto.update({
                "value": purchase_product.value,
                "quantity": purchase_product.quantity
            })

            products.append(dto)

        return products
