from datetime import datetime
from typing import List, Tuple, Optional

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from my_home_server.models.base_models import Base
from my_home_server.models.product_type import ProductType
from my_home_server.models.purchase_product import PurchaseProduct


class Purchase(Base):
    __tablename__ = "purchase"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    purchase_list_id = Column(Integer, ForeignKey("purchase_list.id"), nullable=True)

    created_by = relationship("User", lazy="select")
    purchase_list = relationship("PurchaseList", lazy="select")
    products = relationship("PurchaseProduct", lazy="select", cascade="all, delete-orphan")

    total_value = Column(Float, nullable=False, default=0)

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def fill_total_value(self):
        if not self.products or not len(self.products):
            self.total_value = 0
        else:
            self.total_value = sum([p.calculated_value for p in self.products])

    def get_product_type_and_values(self, initial_product_type_values: Optional[List[dict]] = None) -> List[dict]:
        if not self.products or not len(self.products):
            return list()

        product_type_values = list() if not initial_product_type_values else initial_product_type_values

        for purchase_product in self.products:
            product_type = purchase_product.product.product_type
            if not product_type:
                continue

            parent_product_type = product_type.get_root_product_type()

            while parent_product_type:
                self.__fill_product_type_values(product_type_values, parent_product_type,
                                                purchase_product)
                parent_product_type = product_type.get_root_product_type(before_product_type=parent_product_type)

            self.__fill_product_type_values(product_type_values, product_type, purchase_product)

        return product_type_values

    @staticmethod
    def __fill_product_type_values(product_type_values: List[dict], product_type: ProductType,
                                   purchase_product: PurchaseProduct):
        product_type_value = next((p for p in product_type_values if p["product_type"] == product_type),
                                  None)
        if product_type.is_root():
            if not product_type_value:
                product_type_value = {"product_type": product_type, "value": purchase_product.calculated_value,
                                      "children": []}
                product_type_values.append(product_type_value)
            else:
                product_type_value["value"] += purchase_product.calculated_value
        else:
            parent_product_type_value = next((p for p in product_type_values
                                              if p["product_type"] == product_type.get_root_product_type()),
                                             None)

            product_type_value = next((p for p in parent_product_type_value["children"]
                                       if p["product_type"] == product_type), None)
            if not product_type_value:
                parent_product_type_value["children"].append({
                    "product_type": product_type,
                    "value": purchase_product.calculated_value,
                    "children": []
                })
            else:
                product_type_value["value"] += purchase_product.calculated_value
