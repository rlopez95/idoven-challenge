import uuid
from idoven_app.idoven.domain.command import Command
from idoven_app.idoven.domain.command_handler import CommandHandler
from idoven_app.idoven.domain.command_response import CommandResponse
from idoven_app.idoven.domain.user import User, UserNotFoundException
from idoven_app.idoven.domain.user_repository import UserRepository


class FindUserCommand(Command):
    def __init__(self, username: str) -> None:
        self.username = username
        super().__init__(uuid.uuid1())


class FindUserCommandResponse(CommandResponse):
    def __init__(self, user: User) -> None:
        self.user = user


class FindUserCommandHandler(CommandHandler):
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def process(self, command: FindUserCommand) -> FindUserCommandResponse:
        user = await self._user_repository.find_by_username(command.username)
        if not user:
            raise UserNotFoundException()
        return FindUserCommandResponse(user)
