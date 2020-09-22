from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from my_home_server.models.base_models import Base


class Purchase(Base):
    __tablename__ = "purchase"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    purchase_list_id = Column(Integer, ForeignKey("purchase_list.id"), nullable=True)

    created_by = relationship("User", lazy="select")
    purchase_list = relationship("PurchaseList", lazy="select")
    products = relationship("PurchaseProduct", lazy="select")

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)
