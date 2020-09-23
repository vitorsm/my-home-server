from typing import Optional

from my_home_server.dao.dao import DAO
from my_home_server.models.user import User


class UserDAO(DAO):
    def find_by_id(self, user_id: int) -> Optional[User]:
        return self.db.session.query(User).get(user_id)

    def find_by_login(self, login: str) -> Optional[User]:
        return self.db.session.query(User).filter(User.login == login).first()
