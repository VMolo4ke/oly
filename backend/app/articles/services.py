import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

from app.articles.models import ArticleModel, ArticleChunkModel
from app.articles.schemas import ArticleCreate
from app.users.models import UserModel

embedding_model = SentenceTransformer("sentence-transformers/LaBSE")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)


def _chunk_and_embed(text: str) -> tuple[list[str], list[list[float]]]:
    chunks = text_splitter.split_text(text)
    if not chunks:
        return [], []
    embeddings = embedding_model.encode(chunks).tolist()
    return chunks, embeddings


class ArticleService:
    @staticmethod
    async def create(
        db: AsyncSession,
        article_data: ArticleCreate,
        user: UserModel,
    ) -> ArticleModel:
        db_article = ArticleModel(
            title=article_data.title,
            authors=article_data.authors,
            url=article_data.url,
            context=article_data.context,
            user_id=user.id,
        )
        db.add(db_article)
        await db.flush()

        chunks, embeddings = await asyncio.to_thread(
            _chunk_and_embed, article_data.context
        )

        for text_chunk, vector in zip(chunks, embeddings):
            db.add(
                ArticleChunkModel(
                    article_id=db_article.id,
                    text_content=text_chunk,
                    embedding=vector,
                )
            )

        await db.commit()
        await db.refresh(db_article)
        return db_article

    @staticmethod
    async def get_all(db: AsyncSession) -> Sequence[ArticleModel]:
        result = await db.execute(
            select(ArticleModel)
        )
        return result.scalars().all()
