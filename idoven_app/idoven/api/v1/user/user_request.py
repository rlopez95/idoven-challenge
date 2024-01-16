from pydantic import BaseModel, UUID1
from idoven_app.idoven.domain.user import Role


class UserRequest(BaseModel):
    user_id: UUID1
    username: str
    password: str
    role: Role
    
