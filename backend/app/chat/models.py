import uuid
from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base

class ChatModel(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    owner = relationship("UserModel", back_populates="chats")
    messages = relationship("MessageModel", back_populates="chat")


# TODO: Если нагрузка на LLM-историю вырастет, вынести этот класс в Message Service
class MessageModel(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid7, index=True)
    content = Column(Text, nullable=False)
    role = Column(String, nullable=False, index=True)
    created_at =Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    chat_id = Column(Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False, index=True)
    chat = relationship("ChatModel", back_populates="messages")

