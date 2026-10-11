from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.articles.schemas import ArticleCreate, ArticleResponse
from app.articles.services import ArticleService
from app.core.database import get_db
from app.core.deps import get_current_user
from app.users.models import UserModel

router = APIRouter(prefix="/articles", tags=["Articles"])


@router.post("/upload", response_model=ArticleResponse)
async def create_article(
    title: str = Form(..., description="Название статьи"),
    authors: str = Form(..., description="Авторы статьи через запятую"),
    url: str = Form(..., description="Ссылка на PubMed/SciSpace"),
    context: str = Form(..., description="Сырой текст статьи (сюда можно слать любые \n и спецсимволы)"),
    db: AsyncSession = Depends(get_db),
):
    """
    Эндпоинт принимает данные в формате multipart/form-data (Form).
    Это позволяет отправлять тексты любого объема с любыми переносами строк.
    """
    article_data = ArticleCreate(
        title=title,
        authors=authors,
        url=url,
        context=context
    )
    
    return await ArticleService.create(db, article_data)

@router.get("/", response_model=list[ArticleResponse])
async def read_articles(
    db: AsyncSession = Depends(get_db)
):
    return await ArticleService.get_all(db)


@router.get("/{article_id}", response_model=ArticleResponse)
async def read_article(
    article_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await ArticleService.get_one(article_id, db)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: int, 
    db: AsyncSession = Depends(get_db)
):
    """
    Эндпоинт для удаления статьи по её ID.
    Если статья успешно удалена, возвращает статус 204 No Content.
    Если статьи нет в базе, возвращает ошибку 404 Not Found.
    """
    deleted_article = await ArticleService.delete(id=article_id, db=db)
    
    if deleted_article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Статья с ID {article_id} не найдена в базе данных"
        )
        
    return None