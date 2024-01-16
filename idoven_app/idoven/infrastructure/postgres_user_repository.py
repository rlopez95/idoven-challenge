from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool
from idoven_app.idoven.domain.user import Role, User
from idoven_app.idoven.domain.user_repository import UserRepository


class PostgresUserRepository(UserRepository):
    _TABLE_NAME = "users"

    def __init__(self, postgres_uri: str):
        self._connection_uri = postgres_uri

    async def find_by_username(self, username: str) -> User | None:
        async with AsyncConnectionPool(self._connection_uri) as pool:
            async with pool.connection() as conn:
                async with conn.cursor(row_factory=dict_row) as cur:
                    query = f"SELECT * FROM {PostgresUserRepository._TABLE_NAME} WHERE username = %s"
                    await cur.execute(query, (username,))
                    user = await cur.fetchone()
                    return PostgresUserRepository._create_user(user) if user else None

    async def save(self, user: User) -> None:
        async with AsyncConnectionPool(self._connection_uri) as pool:
            async with pool.connection() as conn:
                async with conn.cursor() as cur:
                    data = user.to_dict()
                    query = f"""INSERT INTO {PostgresUserRepository._TABLE_NAME} (user_id, username, hashed_password, role) 
                    VALUES (%(user_id)s, %(username)s, %(hashed_password)s, %(role)s)"""
                    await cur.execute(query, data)

    @staticmethod
    def _create_user(user: dict) -> User:
        return User(
            user_id=user["user_id"],
            username=user["username"],
            hashed_password=user["hashed_password"],
            role=Role[user["role"]],
        )
