from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.users.models import UserModel
from app.users.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def read_me(current_user: UserModel = Depends(get_current_user)):
    return current_user
