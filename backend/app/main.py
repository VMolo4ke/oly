from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from contextlib import asynccontextmanager

from app.core.database import engine, Base
from app.users.models import UserModel  # noqa: F401
from app.articles.models import ArticleModel, ArticleChunkModel  # noqa: F401
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.articles.router import router as articles_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(
            text(
                "ALTER TABLE articles "
                "ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id) ON DELETE SET NULL"
            )
        )
    yield


app = FastAPI(title="Scientific RAG API (Feature-Based)", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(articles_router, prefix="/api/v1")
