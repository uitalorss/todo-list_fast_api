from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class TaskBase(BaseModel):
    description: str
    completed: bool

class Task(TaskBase):
    int: UUID

class TaskUpdate(BaseModel):
    description: str

class TaskUpdateStatus(BaseModel):
    completed: bool