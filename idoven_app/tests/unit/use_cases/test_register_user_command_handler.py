from unittest.mock import AsyncMock
from idoven_app.idoven.domain.user_repository import UserRepository
from idoven_app.idoven.use_cases.register_user_command import RegisterUserCommand, RegisterUserCommandHandler
from idoven_app.tests.helper.test_user_builder import UserBuilder, TestUserData


async def test_register_user():
    user = UserBuilder().build()
    command = RegisterUserCommand(
        user_id=TestUserData.ANY_USER_ID,
        username=TestUserData.ANY_USER_NAME,
        password=TestUserData.ANY_PASSWORD,
        role=TestUserData.ANY_ROLE,
    )

    repository = AsyncMock(UserRepository)
    register_user_command_handler = RegisterUserCommandHandler(user_repository=repository)
    await register_user_command_handler.process(command)

    repository.save.assert_awaited_once()
    actual_user = repository.save.call_args[0][0]
    assert actual_user.user_id == user.user_id
    assert actual_user.verify_password(TestUserData.ANY_PASSWORD)
    assert actual_user.username == user.username
    assert actual_user.role == user.role
