from typing import List

from my_home_server.mappers.mapper import Mapper
from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.models.purchase import Purchase
from my_home_server.models.purchase_list import PurchaseList
from my_home_server.models.purchase_product import PurchaseProduct
from my_home_server.models.user import User


class PurchaseMapper(MapperInterface):
    def to_dto(self, obj: Purchase) -> dict:
        return {
            "id": obj.id,
            "name": obj.name,
            "created_at": obj.created_by,
            "created_by": Mapper.map_to_dto(obj.created_by),
            "purchase_list": Mapper.map_to_dto(obj.purchase_list),
            "products": self.__products_to_dto(obj.products)
        }

    def to_object(self, dto: dict) -> Purchase:
        purchase = Purchase()
        purchase.id = dto.get("id")
        purchase.name = dto.get("name")
        purchase.created_at = dto.get("created_at")
        purchase.created_by = Mapper.map_to_obj(dto.get("created_by"), User.__name__)
        purchase.purchase_list = Mapper.map_to_obj(dto.get("purchase_list"), PurchaseList.__name__)
        purchase.products = self.__products_to_obj(dto.get("products"))

        return purchase

    def validate_dto(self, dto: dict):
        Mapper.validate_dto(dto, ["name", "products"], Purchase.__name__)

    @staticmethod
    def __products_to_obj(purchase_products_dto: List[dict]) -> List[PurchaseProduct]:
        products = list()
        for dto in purchase_products_dto:
            purchase_product = PurchaseProduct()
            purchase_product.product = Mapper.map_to_obj(dto, PurchaseProduct.__name__)
            purchase_product.quantity = dto.get("quantity")
            purchase_product.value = dto.get("value")
            products.append(purchase_product)

        return products

    @staticmethod
    def __products_to_dto(purchase_products: List[PurchaseProduct]) -> List[dict]:
        products = list()
        for purchase_product in purchase_products:
            dto = Mapper.map_to_dto(purchase_product.product)
            dto.update({
                "value": purchase_product.value,
                "quantity": purchase_product.quantity
            })

            products.append(dto)

        return products
