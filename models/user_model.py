import uuid
from sqlalchemy import Column, String, Integer, Boolean, Date, func, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from core.configs import settings

class UserModel(settings.DBBaseModel):
    __tablename__ = "Usuarios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(256), nullable=False)
    email = Column(String(256), nullable=False, unique=True, index=True)
    password = Column(String(256), nullable=False)