from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import UserModel


class UserService:
    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> UserModel | None:
        result = await db.execute(select(UserModel).where(UserModel.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> UserModel | None:
        result = await db.execute(select(UserModel).where(UserModel.email == email))
        return result.scalar_one_or_none()
