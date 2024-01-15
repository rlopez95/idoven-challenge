from abc import ABC, abstractmethod
from idoven_app.idoven.domain.user import User


class UserRepository(ABC):
    @abstractmethod
    async def find_by_username(self, username: str) -> User | None:
        raise NotImplementedError()

    @abstractmethod
    async def save(self, user: User) -> None:
        raise NotImplementedError()
