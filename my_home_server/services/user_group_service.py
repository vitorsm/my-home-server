from typing import Optional

from my_home_server.dao.user_group_dao import UserGroupDAO
from my_home_server.models.user_group import UserGroup


class UserGroupService(object):
    user_group_dao: UserGroupDAO

    def find_by_id(self, user_group_id: int) -> Optional[UserGroup]:
        return self.user_group_dao.find_by_id(user_group_id)
