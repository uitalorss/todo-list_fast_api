from pydantic import BaseModel
from datetime import datetime

from models.task_model import StatusEnum

class TaskBaseSchema(BaseModel):
    description: str

class TaskSchema(TaskBaseSchema):
    id: int
    status: StatusEnum
    created_at: datetime

    class Config:
        from_attributes=True

class TaskUpdateSchema(BaseModel):
    description: str

class TaskUpdateStatusSchema(BaseModel):
    status: StatusEnum