from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.database import Base

class ArticleModel(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    authors = Column(String)
    url = Column(String, nullable=True)
    context = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    owner = relationship("UserModel", back_populates="articles")
    chunks = relationship("ArticleChunkModel", back_populates="article", cascade="all, delete-orphan")


class ArticleChunkModel(Base):
    __tablename__ = "article_chunks"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    text_content = Column(Text, nullable=False)

    embedding = Column(Vector(768), nullable=False) 

    article = relationship("ArticleModel", back_populates="chunks")