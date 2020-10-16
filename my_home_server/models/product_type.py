from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from my_home_server.models.base_models import Base


class ProductType(Base):
    __tablename__ = "product_type"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    parent_product_type_id = Column(Integer, ForeignKey("product_type.id"))
    is_private = Column(Boolean, nullable=False, default=True)
    created_by_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    parent_product_type = relationship("ProductType", remote_side=[id])
    product_type_children = relationship("ProductType", cascade="all, delete-orphan")

    created_by = relationship("User", lazy="select")

    def __eq__(self, other):
        return type(other) == ProductType and self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def is_root(self):
        return not self.parent_product_type

    def get_root_product_type(self, before_product_type=None, product_type=None):
        if not product_type:
            product_type = self
            if not product_type.parent_product_type or product_type.parent_product_type == before_product_type:
                return None

        if not product_type.parent_product_type:
            return product_type if before_product_type != product_type else None
        elif product_type.parent_product_type == before_product_type:
            return product_type
        else:
            return self.get_root_product_type(before_product_type, product_type.parent_product_type)
