from pydantic import BaseModel, ConfigDict
from typing import Optional


class ArticleCreate(BaseModel):
    title: str
    authors: str
    url: Optional[str] = None
    context: str


class ArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    authors: str
    url: Optional[str] = None
    context: str
    user_id: Optional[int] = None
