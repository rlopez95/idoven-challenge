import asyncio
from idoven_app.idoven.domain.user import User
from idoven_app.idoven.domain.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    _lock = asyncio.Lock()

    def __init__(self) -> None:
        self._users: dict[tuple(str, str), User] = {}

    async def find_by_username(self, username: str) -> User | None:
        return self._users.get(username)

    async def save(self, user: User) -> None:
        async with InMemoryUserRepository._lock:
            self._users[user.username] = user
