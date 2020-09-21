from datetime import datetime

from my_home_server.models.user import User


class AuthenticationData(object):
    user_id: int
    expires_at: datetime
    user_group_id: int

    def __init__(self, user_id: int, expires_at: datetime, user_group_id: int):
        self.user_id = user_id
        self.expires_at = expires_at
        self.user_group_id = user_group_id

    @staticmethod
    def instantiate_by_dto(dto: dict):
        return AuthenticationData(user_id=dto["user_id"], expires_at=dto["expires_at"],
                                  user_group_id=dto["user_group_id"])

    def to_dto(self) -> dict:
        return {
            "user_id": self.user_id,
            "expires_at": self.expires_at,
            "user_group_id": self.user_group_id
        }