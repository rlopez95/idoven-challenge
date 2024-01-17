import uuid
from idoven_app.idoven.infrastructure.postgres_user_repository import PostgresUserRepository
from idoven_app.tests.helper.test_user_builder import UserBuilder
from idoven_app.idoven.config import settings


async def test_save_a_user():
    user_id = str(uuid.uuid1())
    print(f"user id en test nuevo {user_id}")
    username = "nickname"
    user = UserBuilder().build_user_with_user_id(user_id).build_user_with_username(username).build()
    repository = PostgresUserRepository(settings.postgres_uri)
    await repository.save(user)
    new_user = await repository.find_by_username(username)
    assert new_user
    assert str(new_user.user_id) == user_id
    assert new_user.username == username
