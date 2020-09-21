from typing import Optional

from my_home_server.dao.user_group_dao import UserGroupDAO
from my_home_server.models.user_group import UserGroup


class UserGroupService(object):
    def __init__(self, user_group_dao: UserGroupDAO):
        self.user_group_dao = user_group_dao

    def find_by_id(self, user_group_id: int) -> Optional[UserGroup]:
        return self.user_group_dao.find_by_id(user_group_id)
