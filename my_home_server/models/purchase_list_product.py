from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship, backref

from my_home_server.models.base_models import Base


class PurchaseListProduct(Base):
    __tablename__ = "purchase_list_has_product"
    purchase_list_id = Column(Integer, ForeignKey("purchase_list.id"), primary_key=True, nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), primary_key=True, nullable=False)
    estimated_value = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    purchase_list = relationship("PurchaseList", lazy="select", foreign_keys=[purchase_list_id],
                                 back_populates="purchase_products")
    product = relationship("Product", lazy="select", foreign_keys=[product_id])

    def __eq__(self, other):
        return other and self.purchase_list_id == other.purchase_list_id and self.product_id == other.product_id

    def __hash__(self):
        return hash(self.purchase_list_id + self.product_id)
