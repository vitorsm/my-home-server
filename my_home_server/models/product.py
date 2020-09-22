from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from my_home_server.models.base_models import Base


class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    product_type_id = Column(Integer, ForeignKey("product_type.id"))
    brand_id = Column(Integer, ForeignKey("brand.id"))
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    is_private = Column(Boolean, nullable=False, default=True)
    image_url = Column(String, nullable=True)

    product_type = relationship("ProductType", lazy="select")
    brand = relationship("Brand", lazy="select")
    created_by = relationship("User", lazy="select")

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)
