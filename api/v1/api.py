from fastapi import APIRouter

from .endpoints import user, task

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["Usuários"])
api_router.include_router(task.router, prefix="/tasks", tags=["Tarefas"])