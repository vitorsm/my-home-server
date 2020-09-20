from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from my_home_server.models.base_models import Base


class PurchaseList(Base):
    __tablename__ = "purchase_list"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_by = relationship("User", lazy="select")
    purchase_products = relationship("ProductListProduct", lazy="select")

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)
