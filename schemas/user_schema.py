from typing import Optional, List
from pydantic import BaseModel, EmailStr
from schemas.task_schema import Task

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    int: str

    class Config:
        from_attributes=True

class UserCreate(UserBase):
    password: str

class UserUpdate(User):
    int: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    password: Optional[str] = None

class UserListTasks(UserBase):
    tasks: List[Task]