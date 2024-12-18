from fastapi import HTTPException, status, Response
from fastapi.exceptions import ResponseValidationError

from core.auth.security import generate_hashed_password
from core.auth.security import verify_password
from core.auth.auth import create_access_token
from schemas.user_schema import UserSchema, UserBaseSchema, UserCreateSchema, UserUpdateSchema, UserLoginSchema
from models.user_model import UserModel

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

async def create_user(user: UserCreateSchema, db: AsyncSession):
    new_user: UserModel = UserModel(name=user.name, email=user.email, password=generate_hashed_password(user.password))

    async with db as session:
        try:
            session.add(new_user)
            await session.commit()

            return new_user
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado.")
        
async def get_user(user_id: UUID, db: AsyncSession):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserSchema = result.scalars().unique().one_or_none()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
        
        return user
    
async def update_user(user_id: UUID, user: UserUpdateSchema, db: AsyncSession):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_to_update: UserSchema = result.scalars().unique().one_or_none()

        if user_to_update is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")

        if user.name:
            user_to_update.name = user.name

        if user.email:
            user_to_update.email = user.email

        if user.password:
            user_to_update.password = generate_hashed_password(user.password)

        await session.commit()

        return user_to_update
    
async def delete_user(user_id: UUID, db: AsyncSession):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_to_delete: UserSchema = result.scalars().unique().one_or_none()

        if user_to_delete is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        await session.delete(user_to_delete)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
async def login_user(user_login: UserLoginSchema, db: AsyncSession):
    async with db as session:
        query = select(UserModel).filter(UserModel.email == user_login.email)
        result = await session.execute(query)
        user = result.scalars().unique().one_or_none()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário e/ou senha incorretos.")
        
        if not verify_password(user_login.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário e/ou senha incorretos.")
        
        user_id = str(user.id)

        return create_access_token(sub=user_id)