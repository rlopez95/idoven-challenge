import uuid
from enum import StrEnum
from dataclasses import dataclass, asdict


class Role(StrEnum):
    USER = "USER"
    ADMIN = "ADMIN"


@dataclass
class User:
    user_id: str
    username: str
    password: str
    role: Role

    def to_dict(self) -> dict:
        return asdict(self)


class UserFactory:
    @staticmethod
    def make(user_id: str, username: str, password: str, role: Role) -> User:
        try:
            uuid.UUID(user_id)
        except ValueError as e:
            raise UserInvalidException("Invalid uuid for user id") from e

        if not username:
            raise UserInvalidException("User must have a username")

        if not password:
            raise UserInvalidException("User must have a password")

        if not role or role not in Role.__members__.values():
            raise UserInvalidException("User must have a valid role")

        return User(user_id=user_id, username=username, password=password, role=role)


class UserInvalidException(Exception):
    pass
