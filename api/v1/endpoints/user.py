from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user_schema import UserCreateSchema, UserSchema, UserUpdateSchema, UserLoginSchema
from services.user_service import create_user, delete_user, update_user, get_user, login_user
from models.user_model import UserModel

from core.auth.deps import get_session, get_current_user

router = APIRouter()

@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def post(user: UserCreateSchema, db: AsyncSession = Depends(get_session)):
    return await create_user(user, db)

@router.post("/login", status_code=status.HTTP_201_CREATED)
async def post_login(user: UserLoginSchema, db: AsyncSession = Depends(get_session)):

    token = await login_user(user_login=user, db=db)
    return JSONResponse(content = {"access_token": token, "token-type": "bearer"}, status_code=status.HTTP_200_OK) 

@router.get("/", response_model=UserSchema, status_code=status.HTTP_200_OK)
async def get(db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    return await get_user(user_id=logged_user.id, db=db)

@router.put("/", response_model=UserSchema, status_code=status.HTTP_202_ACCEPTED)
async def put(user: UserUpdateSchema, db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    return await update_user(user_id=logged_user.id, user=user, db=db)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(db: AsyncSession = Depends(get_session), logged_user: UserModel = Depends(get_current_user)):
    return await delete_user(user_id = logged_user.id, db=db)