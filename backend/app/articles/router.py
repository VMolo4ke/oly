from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.articles.schemas import ArticleCreate, ArticleResponse
from app.articles.services import ArticleService
from app.core.database import get_db
from app.core.deps import get_current_user
from app.users.models import UserModel

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.post("/upload", response_model=ArticleResponse)
async def create_article(
    article: ArticleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await ArticleService.create(db, article, current_user)


@router.get("/", response_model=list[ArticleResponse])
async def read_articles(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return await ArticleService.get_all(db, current_user)
