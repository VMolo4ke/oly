from pydantic import BaseModel
from typing import Optional

class ArticleCreate(BaseModel):
    title: str
    authors: str
    url: Optional[str] = None
    context: str

class ArticleResponse(BaseModel):
    id: int
    title: str
    authors: str
    url: Optional[str] = None
    context: str

    class Config:
        from_attributes = True
