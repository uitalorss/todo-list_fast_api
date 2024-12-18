from enum import Enum

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
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
    status = Column(SQLAlchemyEnum(), nullable=False, default=StatusEnum.NAO_INICIADO)
    created_at = Column(DateTime, default=datetime.now(timezone("America/Bahia")))