from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.articles.models import ArticleModel
from app.articles.schemas import ArticleCreate

class ArticleService:
    @staticmethod
    async def create(db: AsyncSession, article_data: ArticleCreate) -> ArticleModel:
        db_article = ArticleModel(
            title=article_data.title,
            authors=article_data.authors,
            url=article_data.url,
            content=article_data.content
        )
        db.add(db_article)
        await db.commit()
        await db.refresh(db_article)
        return db_article

    @staticmethod
    async def get_all(db: AsyncSession) -> List[ArticleModel]:
        result = await db.execute(select(ArticleModel))
        return result.scalars().all()
