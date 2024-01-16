import uuid
from idoven_app.idoven.domain.command_handler import CommandHandler
from idoven_app.idoven.domain.command import Command
from idoven_app.idoven.domain.command_response import CommandResponse
from idoven_app.idoven.domain.user_repository import UserRepository
from idoven_app.idoven.domain.user import Role, User, UserFactory


class RegisterUserCommand(Command):
    def __init__(self, user_id: str, username: str, password: str, role: Role) -> None:
        self.user_id = user_id
        self.username = username
        self.password = password
        self.role = role
        super().__init__(uuid.uuid1())


class RegisterUserCommandResponse(CommandResponse):
    pass


class RegisterUserCommandHandler(CommandHandler):
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def process(self, command: RegisterUserCommand) -> RegisterUserCommandResponse:
        user = UserFactory.make(
            user_id=command.user_id,
            username=command.username,
            password=command.password,
            role=command.role,
        )
        await self._user_repository.save(user)
        return RegisterUserCommandResponse()
