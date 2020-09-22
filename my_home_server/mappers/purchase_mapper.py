from typing import List, Optional

from my_home_server.mappers.mapper_interface import MapperInterface
from my_home_server.mappers.product_mapper import ProductMapper
from my_home_server.mappers.purchase_list_mapper import PurchaseListMapper
from my_home_server.mappers.user_mapper import UserMapper
from my_home_server.models.purchase import Purchase
from my_home_server.models.purchase_product import PurchaseProduct


class PurchaseMapper(MapperInterface):
    def __init__(self):
        self.user_mapper = UserMapper()
        self.product_mapper = ProductMapper()
        self.purchase_list_mapper = PurchaseListMapper()

    def to_dto(self, obj: Purchase) -> Optional[dict]:
        if not obj:
            return None

        return {
            "id": obj.id,
            "name": obj.name,
            "created_at": obj.created_by,
            "created_by": self.user_mapper.to_dto(obj.created_by),
            "purchase_list": self.purchase_list_mapper.to_dto(obj.purchase_list),
            "products": self.__products_to_dto(obj.products)
        }

    def to_object(self, dto: dict, loaded_object: Purchase = None) -> Optional[Purchase]:
        if not dto:
            return None

        purchase = loaded_object if loaded_object else Purchase()
        purchase.id = dto.get("id")
        purchase.name = dto.get("name")
        purchase.purchase_list = self.purchase_list_mapper.to_object(dto.get("purchase_list"))
        purchase.products = self.__products_to_obj(dto.get("products"))

        if not loaded_object:
            purchase.created_at = dto.get("created_at")
            purchase.created_by = self.user_mapper.to_object(dto.get("created_by"))

        return purchase

    def get_required_fields_to_insert(self):
        return ["name"]

    def get_required_fields_to_update(self):
        return ["id", "name", "products"]

    def get_entity_name(self):
        return Purchase.__name__

    def __products_to_obj(self, purchase_products_dto: List[dict]) -> List[PurchaseProduct]:
        products = list()
        for dto in purchase_products_dto:
            purchase_product = PurchaseProduct()
            purchase_product.product = self.product_mapper.to_object(dto)
            purchase_product.quantity = dto.get("quantity")
            purchase_product.value = dto.get("value")
            products.append(purchase_product)

        return products

    def __products_to_dto(self, purchase_products: List[PurchaseProduct]) -> List[dict]:
        products = list()
        for purchase_product in purchase_products:
            dto = self.product_mapper.to_dto(purchase_product.product)
            dto.update({
                "value": purchase_product.value,
                "quantity": purchase_product.quantity
            })

            products.append(dto)

        return products
