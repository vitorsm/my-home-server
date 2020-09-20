from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from my_home_server.models.base_models import Base


class ProductType(Base):
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    parent_product_type = relationship("ProductType", lazy="select")
    is_private = Column(Boolean, nullable=False, default=True)
    created_by = relationship("User", lazy="select")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)
