from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, ValidationError
from fastapi import Depends, APIRouter, HTTPException, status, Security
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jose import JWTError, jwt
from passlib.context import CryptContext
from idoven_app.idoven.config import settings


SECRET_KEY = "adba27e22c8cff65dd8e713bce6383c789eadcae6c95945ceab3c94a2697b8d9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "$2b$12$b2YV8Q8TuHS1Hfrrtf1EFehdYYtqz2xN3HjTEi1LFjkxdZzQrJsni", # password1
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "hashed_password": "$2b$12$IY7mAOnXN3HSEp1QJcWP0OU3t2RFbbxj3Eo8fS0dGJy7nT/2bOxqu", # password2
        "disabled": True,
    },
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class User(BaseModel):
    username: str
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str
    role: str = "USER"


auth_router = APIRouter(prefix=settings.api_v1_prefix)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_v1_prefix}/token",
    scopes={"USER": "Read information about user ECG.", "ADMIN": "Creates new users."},
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    if user := get_user(fake_db, username):
        return user if verify_password(password, user.hashed_password) else False
    else:
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError) as e:
        raise credentials_exception from e
    user = get_user(fake_users_db, username=token_data.username)
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


async def get_current_active_user(
    current_user: User = Security(get_current_user, scopes=["USER"])
):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


@auth_router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": [user.role]},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.get("/users/me/items/")
async def read_own_items(
    current_user: User = Security(get_current_active_user, scopes=["USER"])
):
    return [{"item_id": "Foo", "owner": current_user.username}]