from typing import Self
from uuid import uuid1
from passlib.context import CryptContext
from idoven_app.idoven.domain.user import User, Role, UserFactory

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TestUserData:
    ANY_USER_ID = str(uuid1())
    ANY_USER_NAME = "testuser"
    ANY_PASSWORD = "pwd"
    ANY_ROLE = Role.USER


class UserBuilder:
    def __init__(self) -> None:
        self._user_id = TestUserData.ANY_USER_ID
        self._username = TestUserData.ANY_USER_NAME
        self._password = TestUserData.ANY_PASSWORD
        self._role = TestUserData.ANY_ROLE

    def build_user_with_user_id(self, user_id: str) -> Self:
        self._user_id = user_id
        return self

    def build_user_with_username(self, username: str) -> Self:
        self._username = username
        return self

    def build_user_with_password(self, password: str) -> Self:
        self._password = password
        return self

    def build_user_with_role(self, role: Role) -> Self:
        self._role = role
        return self

    def build(self) -> User:
        return UserFactory.make(
            user_id=self._user_id, username=self._username, password=self._password, role=self._role
        )
