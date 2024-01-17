from datetime import datetime
from idoven_app.idoven.infrastructure.in_memory_user_repository import (
    InMemoryUserRepository,
)
from idoven_app.tests.helper.test_user_builder import UserBuilder, TestUserData


async def test_find_user_by_username():
    repository = InMemoryUserRepository()
    user = (
        UserBuilder()
        .build_user_with_user_id(TestUserData.ANY_USER_ID)
        .build_user_with_username(TestUserData.ANY_USER_NAME)
        .build()
    )

    await repository.save(user)
    actual_user = await repository.find_by_username(TestUserData.ANY_USER_NAME)

    assert actual_user == user
    assert actual_user.user_id == TestUserData.ANY_USER_ID
    assert actual_user.username == TestUserData.ANY_USER_NAME


async def test_save_user():
    repository = InMemoryUserRepository()
    user = (
        UserBuilder()
        .build_user_with_user_id(TestUserData.ANY_USER_ID)
        .build_user_with_username(TestUserData.ANY_USER_NAME)
        .build_user_with_role(TestUserData.ANY_ROLE)
        .build()
    )

    await repository.save(user)
    actual_user = await repository.find_by_username(TestUserData.ANY_USER_NAME)

    assert actual_user == user
    assert actual_user.username == TestUserData.ANY_USER_NAME
    assert actual_user.user_id == TestUserData.ANY_USER_ID
    assert actual_user.role == TestUserData.ANY_ROLE
