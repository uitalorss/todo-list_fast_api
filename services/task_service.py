from fastapi import status, HTTPException, Response

from models.task_model import TaskModel, StatusEnum

from schemas.task_schema import TaskBaseSchema, TaskSchema, TaskUpdateSchema, TaskUpdateStatusSchema

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from uuid import UUID

async def create_task(task: TaskBaseSchema, user_id: UUID,  db: AsyncSession):
    new_task: TaskModel = TaskModel(description=task.description, user_id=user_id, status=StatusEnum.NAO_INICIADO.value)

    async with db as session:
        try:
            session.add(new_task)
            await session.commit()
            print(type(new_task.id))
            return new_task
        except IntegrityError:
            raise HTTPException("Erro ao criar tarefa")

async def get_task(task_id: int, db: AsyncSession):
    async with db as session:
        query = select(TaskModel).filter(TaskModel.id == task_id)
        result = await session.execute(query)
        task = result.scalars().unique().one_or_none()

        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada.")
        
        return task
    
async def update_task(task_id: int, task: TaskUpdateSchema, db: AsyncSession):
    async with db as session:
        query = select(TaskModel).filter(TaskModel.id == task_id)
        result = await session.execute(query)
        update_task_data = result.scalars().unique().one_or_none()

        if update_task_data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada.")
        
        update_task_data.description = task.description

        await session.commit()

        return update_task_data

async def update_status_task(task_id: int, task: TaskUpdateStatusSchema, db: AsyncSession):
    print
    async with db as session:
        query = select(TaskModel).filter(TaskModel.id == task_id)
        result = await session.execute(query)
        update_task_data = result.scalars().unique().one_or_none()

        if update_task_data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada.")
        
        update_task_data.status = task.status

        await session.commit()

        return update_task_data
    

async def delete_task(task_id: int, db: AsyncSession):
    async with db as session:
        query = select(TaskModel).filter(TaskModel.id == task_id)
        result = await session.execute(query)
        delete_task_data: TaskModel = result.scalars().unique().one_or_none()

        if delete_task_data is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada.")
        
        await session.delete(delete_task_data)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)