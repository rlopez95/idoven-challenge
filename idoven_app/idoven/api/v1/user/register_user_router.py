from fastapi import APIRouter, Depends, HTTPException, Security, status
from idoven_app.idoven.api.v1.auth import get_current_user
from idoven_app.idoven.api.v1.user.user_request import UserRequest
from idoven_app.idoven.domain.user import UserInvalidException
from idoven_app.idoven.domain.command_handler import CommandHandler
from idoven_app.idoven.infrastructure.postgres_user_repository import PostgresUserRepository
from idoven_app.idoven.use_cases.register_user_command import RegisterUserCommand
from idoven_app.idoven.use_cases.register_user_command import RegisterUserCommandHandler, RegisterUserCommandResponse
from idoven_app.idoven.config import settings

register_user_router = APIRouter(prefix=settings.api_v1_prefix)


async def _register_user_command_handler() -> CommandHandler:
    repository = PostgresUserRepository(postgres_uri=settings.postgres_uri)
    return RegisterUserCommandHandler(repository)


@register_user_router.post("/user", status_code=status.HTTP_201_CREATED)
async def register_ecg(
    user_request: UserRequest = Security(get_current_user, scopes=["USER"]),
    register_user_command_handler: CommandHandler = Depends(_register_user_command_handler),
):
    try:
        command = RegisterUserCommand(
            user_id=user_request.user_id,
            username=user_request.username,
            password=user_request.password,
            role=user_request.role,
        )
        await register_user_command_handler.process(command)
    except UserInvalidException as invalid_exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"""The user with id: {user_request.user_id}, 
            username: {user_request.username} 
            password {user_request.password} 
            and role {user_request.role} is invalid""",
        ) from invalid_exception
