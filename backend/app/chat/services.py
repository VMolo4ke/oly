import asyncio
import json
from collections.abc import AsyncIterator

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.articles.models import ArticleChunkModel, ArticleModel
from app.articles.services import embedding_model
from app.chat.schemas import ChatHistoryItem
from app.core.config import settings
from app.users.models import UserModel

SYSTEM_PROMPT = (
    "Ты — помощник по научным статьям. Отвечай на языке вопроса, опираясь на "
    "приведённый контекст из статей пользователя. Если в контексте нет ответа, "
    "честно скажи об этом и ответь исходя из общих знаний, пометив это."
)


class LLMError(Exception):
    """Ошибка при обращении к LLM-провайдеру."""


class ChatService:
    @staticmethod
    async def retrieve_context(
        db: AsyncSession, user: UserModel, query: str
    ) -> list[tuple[ArticleModel, str]]:
        """Ищет ближайшие чанки среди статей пользователя."""
        vector = await asyncio.to_thread(
            lambda: embedding_model.encode([query])[0].tolist()
        )
        stmt = (
            select(ArticleModel, ArticleChunkModel.text_content)
            .join(ArticleChunkModel, ArticleChunkModel.article_id == ArticleModel.id)
            .where(ArticleModel.user_id == user.id)
            .order_by(ArticleChunkModel.embedding.cosine_distance(vector))
            .limit(settings.CHAT_TOP_K)
        )
        result = await db.execute(stmt)
        return [(article, text) for article, text in result.all()]

    @staticmethod
    def build_messages(
        message: str,
        history: list[ChatHistoryItem],
        context: list[tuple[ArticleModel, str]],
    ) -> list[dict[str, str]]:
        system = SYSTEM_PROMPT
        if context:
            blocks = [
                f"[{i}] {article.title} ({article.authors})\n{text}"
                for i, (article, text) in enumerate(context, start=1)
            ]
            system += "\n\nКонтекст:\n\n" + "\n\n".join(blocks)

        messages = [{"role": "system", "content": system}]
        messages += [{"role": h.role, "content": h.content} for h in history]
        messages.append({"role": "user", "content": message})
        return messages

    @staticmethod
    async def stream_completion(messages: list[dict[str, str]]) -> AsyncIterator[str]:
        """Стримит токены из OpenAI-совместимого /chat/completions."""
        headers = {}
        if settings.LLM_API_KEY:
            headers["Authorization"] = f"Bearer {settings.LLM_API_KEY}"
        payload = {"model": settings.LLM_MODEL, "messages": messages, "stream": True}
        url = f"{settings.LLM_BASE_URL.rstrip('/')}/chat/completions"

        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(120, connect=10)) as client:
                async with client.stream(
                    "POST", url, json=payload, headers=headers
                ) as response:
                    if response.status_code != 200:
                        body = (await response.aread()).decode(errors="replace")[:300]
                        raise LLMError(f"LLM вернул {response.status_code}: {body}")

                    async for line in response.aiter_lines():
                        if not line.startswith("data:"):
                            continue
                        data = line[5:].strip()
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                            delta = chunk["choices"][0]["delta"].get("content")
                        except (json.JSONDecodeError, KeyError, IndexError):
                            continue
                        if delta:
                            yield delta
        except httpx.HTTPError as exc:
            raise LLMError("Не удалось связаться с LLM-сервисом") from exc
