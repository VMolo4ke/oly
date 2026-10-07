from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

from app.articles.models import ArticleModel, ArticleChunkModel
from app.articles.schemas import ArticleCreate

embedding_model = SentenceTransformer("sentence-transformers/LaBSE")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

class ArticleService:
    @staticmethod
    async def create(db: AsyncSession, article_data: ArticleCreate) -> ArticleModel:
        db_article = ArticleModel(
            title=article_data.title,
            authors=article_data.authors,
            url=article_data.url,
            context=article_data.context
        )
        db.add(db_article)
        await db.commit()
        await db.refresh(db_article)

        chunks = text_splitter.split_text(article_data.context)

        embeddings = embedding_model.encode(chunks).tolist()

        for text_chunk, vector in zip(chunks, embeddings):
            db_chunk = ArticleChunkModel(
                article_id=db_article.id,
                text_content=text_chunk,
                embedding=vector
            )
            db.add(db_chunk)

        await db.commit()
        return db_article

    @staticmethod
    async def get_all(db: AsyncSession) -> List[ArticleModel]:
        result = await db.execute(select(ArticleModel))
        return result.scalars().all()
