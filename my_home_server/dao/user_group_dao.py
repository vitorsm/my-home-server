from my_home_server.dao.dao import DAO
from my_home_server.models.user_group import UserGroup


class UserGroupDAO(DAO):
    def find_by_id(self, user_group_id: int) -> UserGroup:
        return self.db.session.query(UserGroup).get(user_group_id)
