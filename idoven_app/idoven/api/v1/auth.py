from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, ValidationError
from fastapi import Depends, APIRouter, HTTPException, status, Security
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import JWTError, jwt
from idoven_app.idoven.config import settings
from idoven_app.idoven.domain.command_handler import CommandHandler
from idoven_app.idoven.domain.user import Role, User
from idoven_app.idoven.infrastructure.postgres_user_repository import PostgresUserRepository
from idoven_app.idoven.use_cases.find_user_command import (
    FindUserCommand,
    FindUserCommandHandler,
    FindUserCommandResponse,
)
from idoven_app.idoven.config import settings


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


auth_router = APIRouter(prefix=settings.api_v1_prefix)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_v1_prefix}/token",
    scopes={Role.USER.value: "Read information about user ECG.", Role.ADMIN.value: "Creates new users."},
)


async def _find_user_command_handler() -> CommandHandler:
    repository = PostgresUserRepository(postgres_uri=settings.postgres_uri)
    return FindUserCommandHandler(repository)


async def get_user(
    username: str, find_user_command_handler: CommandHandler = Depends(_find_user_command_handler)
) -> FindUserCommandResponse:
    command = FindUserCommand(username=username)
    user_response: FindUserCommandResponse = await find_user_command_handler.process(command)
    return user_response.user


async def authenticate_user(
    username: str,
    password: str,
    find_user_command_handler: CommandHandler = Depends(_find_user_command_handler),
):
    command = FindUserCommand(username=username)
    user_response: FindUserCommandResponse = find_user_command_handler.process(command)
    if user_response:
        user = user_response.user
        return user if user.verify_password(password) else False
    else:
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorith)


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)) -> User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorith])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError) as e:
        raise credentials_exception from e
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


@auth_router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.token_expiration_time)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": [user.role]},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.get("/users/me/items/")
async def read_own_items(current_user: User = Security(get_current_user, scopes=[Role.USER])):
    return [{"item_id": "Foo", "owner": current_user.username}]
