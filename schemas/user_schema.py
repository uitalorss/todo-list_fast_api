from typing import Optional, List
from pydantic import BaseModel, EmailStr
from schemas.task_schema import Task

class UserBaseSchema(BaseModel):
    email: EmailStr
    name: str

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserSchema(UserBaseSchema):
    int: str

    class Config:
        from_attributes=True

class UserCreateSchema(UserBaseSchema):
    password: str

class UserUpdateSchema(UserSchema):
    int: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None

class UserListTasksSchema(UserBaseSchema):
    tasks: List[Task]