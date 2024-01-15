from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool
from idoven_app.idoven.domain.user import User
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
                    return await cur.fetchone()

    async def save(self, user: User) -> None:
        async with AsyncConnectionPool(self._connection_uri) as pool:
            async with pool.connection() as conn:
                async with conn.cursor() as cur:
                    data = user.to_dict()
                    query = f"""INSERT INTO {PostgresUserRepository._TABLE_NAME} (user_id, username, password, role) 
                    VALUES (%(user_id)s, %(username)s, %(password)s)"""
                    await cur.execute(query, data)
