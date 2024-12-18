from fastapi import APIRouter, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.task_schema import TaskBaseSchema, TaskSchema, TaskUpdateSchema, TaskUpdateStatusSchema
from models.user_model import UserModel
from services.task_service import create_task, get_task, update_task, update_status_task, delete_task

from core.auth.deps import get_session, get_current_user

router = APIRouter()

@router.post("/", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def post_task(task: TaskBaseSchema, db: AsyncSession = Depends(get_session), user: UserModel = Depends(get_current_user)):
    return await create_task(task=task, user_id=user.id, db=db)

@router.get("/{task_id}", response_model=TaskSchema, status_code=status.HTTP_200_OK)
async def get_task_id(task_id: int, db: AsyncSession = Depends(get_session), user: UserModel = Depends(get_current_user)):
    return await get_task(task_id, db, user)

@router.put("/{task_id}", response_model=TaskSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_task(task_id: int, task: TaskUpdateSchema, db: AsyncSession = Depends(get_session), user: UserModel = Depends(get_current_user)):
    return await update_task(task_id, task, db, user)

@router.patch("/{task_id}", response_model=TaskSchema, status_code=status.HTTP_202_ACCEPTED)
async def patch_task(task_id: int, task: TaskUpdateStatusSchema, db: AsyncSession = Depends(get_session), user: UserModel = Depends(get_current_user)):
    return await update_status_task(task_id, task, db, user)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_task(task_id: int, db: AsyncSession =  Depends(get_session), user: UserModel = Depends(get_current_user)):
    return await delete_task(task_id, db, user)