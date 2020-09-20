from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from my_home_server.models.base_models import Base


class UserGroup(Base):
    __tablename__ = "user_group"
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)
