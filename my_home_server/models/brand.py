from sqlalchemy import Column, Integer, String

from my_home_server.models.base_models import Base


class Brand(Base):
    __tablename__ = "brand"
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)

    def __eq__(self, other):
        return other and self.id == other.id

    def __hash__(self):
        return hash(self.id)
