import asyncio

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password
from app.users.models import UserModel
from app.users.services import UserService


class AuthService:
    @staticmethod
    async def register(db: AsyncSession, email: str, password: str) -> UserModel:
        existing = await UserService.get_by_email(db, email.lower())
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

        hashed = await asyncio.to_thread(hash_password, password)
        user = UserModel(email=email.lower(), hashed_password=hashed)
        db.add(user)
        try:
            await db.commit()
        except IntegrityError as exc:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            ) from exc

        await db.refresh(user)
        return user

    @staticmethod
    async def login(db: AsyncSession, email: str, password: str) -> str:
        user = await UserService.get_by_email(db, email.lower())
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        valid = await asyncio.to_thread(verify_password, password, user.hashed_password)
        if not valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        return create_access_token(str(user.id))
