from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from my_home_server.models.base_models import Base


class PurchaseProduct(Base):
    __tablename__ = "purchase_has_product"
    purchase_id = Column(Integer, ForeignKey("purchase.id"), primary_key=True, nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), primary_key=True, nullable=False)
    value = Column(Float, nullable=False, default=0)
    quantity = Column(Integer, nullable=False, default=0)

    purchase = relationship("Purchase", lazy="select")
    product = relationship("Product", lazy="select")

    def __eq__(self, other):
        return other and self.purchase_id == other.purchase_id and self.product_id == other.product_id

    def __hash__(self):
        return hash(self.purchase_id + self.product_id)
