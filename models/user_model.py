import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from core.configs import settings

class UserModel(settings.DBBaseModel):
    __tablename__ = "Usuarios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(256), nullable=False)
    email = Column(String(256), nullable=False, unique=True, index=True)
    password = Column(String(256), nullable=False)
    tasks = relationship("TaskModel", cascade="all,delete-orphan", back_populates="user", uselist=True, lazy="joined")