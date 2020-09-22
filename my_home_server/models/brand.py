from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from my_home_server.models.base_models import Base


class Brand(Base):
    __tablename__ = "brand"
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    is_private = Column(Boolean, nullable=False, default=True)
    created_by_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    created_by = relationship("User", lazy="select")

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)
