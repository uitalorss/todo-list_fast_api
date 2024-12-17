from fastapi import APIRouter, status, Depends

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user_schema import UserCreateSchema, UserSchema, UserUpdateSchema
from services.user_service import create_user, delete_user, update_user, get_user

from core.auth.deps import get_session

router = APIRouter()

@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def post(user: UserCreateSchema, db: AsyncSession = Depends(get_session)):
    return await create_user(user, db)

@router.get("/{user_id}", response_model=UserSchema, status_code=status.HTTP_200_OK)
async def get(user_id: UUID, db: AsyncSession = Depends(get_session)):
    return await get_user(user_id, db)

@router.put("/{user_id}", response_model=UserSchema, status_code=status.HTTP_202_ACCEPTED)
async def put(user_id: UUID, user: UserUpdateSchema, db: AsyncSession = Depends(get_session)):
    return await update_user(user_id, user, db)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(user_id: UUID, db: AsyncSession = Depends(get_session)):
    return await delete_user(user_id, db)