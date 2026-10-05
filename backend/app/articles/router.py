from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.articles.schemas import ArticleCreate, ArticleResponse
from app.articles.services import ArticleService

router = APIRouter(prefix="/articles", tags=["Articles"])

@router.post("/upload", response_model=ArticleResponse)
async def create_article(article: ArticleCreate, db: AsyncSession = Depends(get_db)):
    return await ArticleService.create(db, article)

@router.get("/", response_model=List[ArticleResponse])
async def read_articles(db: AsyncSession = Depends(get_db)):
    return await ArticleService.get_all(db)
