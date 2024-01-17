from pydantic import BaseModel
from idoven_app.idoven.domain.user import Role


class UserRequest(BaseModel):
    user_id: str
    username: str
    password: str
    role: Role
    
