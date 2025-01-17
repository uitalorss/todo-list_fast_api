from enum import Enum

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from core.configs import settings

from datetime import datetime

from pytz import timezone

class StatusEnum(str, Enum):
    NAO_INICIADO = "Não iniciado"
    EM_ANDAMENTO = "Em andamento"
    CONCLUIDO = "Concluído"

class TaskModel(settings.DBBaseModel):
    __tablename__ = "Tarefas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String, nullable=False)
    tag = Column(String)
    status = Column(SQLAlchemyEnum(StatusEnum), nullable=False, default=StatusEnum.NAO_INICIADO.value)
    created_at = Column(DateTime, default=datetime.now(timezone("America/Bahia")))
    user_id = Column(UUID, ForeignKey("Usuarios.id"))
    user = relationship("UserModel", back_populates="tasks", lazy="joined")