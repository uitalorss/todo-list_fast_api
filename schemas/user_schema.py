from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from schemas.task_schema import Task


class UserBaseSchema(BaseModel):
    email: str
    name: str

class UserLoginSchema(BaseModel):
    email: str
    password: str

class UserSchema(UserBaseSchema):
    id: UUID

    class Config:
        from_attributes=True

class UserCreateSchema(UserBaseSchema):
    password: str

class UserUpdateSchema(UserSchema):
    id: Optional[UUID] = None
    email: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None

class UserListTasksSchema(UserBaseSchema):
    tasks: List[Task]