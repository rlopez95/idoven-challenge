from idoven_app.idoven.domain.user import UserNotFoundException
import pytest
from unittest.mock import AsyncMock
from idoven_app.idoven.domain.user_repository import UserRepository
from idoven_app.idoven.use_cases.find_user_command import FindUserCommand, FindUserCommandHandler
from idoven_app.tests.helper.test_user_builder import TestUserData, UserBuilder


async def test_find_user():
    command = FindUserCommand(TestUserData.ANY_USER_NAME)
    repository = AsyncMock(UserRepository)
    repository.find_by_username.return_value = (
        UserBuilder().build_user_with_username(TestUserData.ANY_USER_NAME).build()
    )
    handler = FindUserCommandHandler(repository)
    actual_user = await handler.process(command)

    repository.find_by_username.assert_called_once_with(command.username)

    assert actual_user.user.username == TestUserData.ANY_USER_NAME


async def test_raises_an_error_when_the_user_is_not_found():
    command = FindUserCommand(TestUserData.ANY_USER_NAME)
    repository = AsyncMock(UserRepository)
    repository.find_by_username.return_value = None
    handler = FindUserCommandHandler(repository)

    with pytest.raises(UserNotFoundException):
        await handler.process(command)
