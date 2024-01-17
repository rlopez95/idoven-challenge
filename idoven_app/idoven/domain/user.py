import uuid
from enum import StrEnum
from dataclasses import dataclass, asdict
from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Role(StrEnum):
    USER = "USER"
    ADMIN = "ADMIN"


@dataclass
class User:
    user_id: str
    username: str
    hashed_password: str
    role: Role

    def verify_password(self, plain_password: str) -> bool:
        return _pwd_context.verify(plain_password, self.hashed_password)

    def to_dict(self) -> dict:
        return asdict(self)


class UserFactory:
    @staticmethod
    def make(user_id: str, username: str, password: str, role: Role) -> User:
        try:
            uuid.UUID(user_id, version=1)
        except ValueError as ve:
            raise UserInvalidException("User must have a user_id")

        if not username:
            raise UserInvalidException("User must have a username")

        if not password:
            raise UserInvalidException("User must have a password")

        if not role or role not in Role.__members__.values():
            raise UserInvalidException("User must have a valid role")

        return User(user_id=user_id, username=username, hashed_password=_pwd_context.hash(password), role=role)


class UserInvalidException(Exception):
    pass


class UserAlreadyExistsException(Exception):
    pass


class UserNotFoundException(Exception):
    pass
