from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import TokenResponse, UserLogin, UserRegister
from app.auth.services import AuthService
from app.core.database import get_db
from app.users.schemas import UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(payload: UserRegister, db: AsyncSession = Depends(get_db)):
    return await AuthService.register(db, payload.email, payload.password)


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):
    access_token = await AuthService.login(db, payload.email, payload.password)
    return TokenResponse(access_token=access_token)
