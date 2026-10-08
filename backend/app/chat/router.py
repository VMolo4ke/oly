from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from app.chat.schemas import ChatClientMessage
from app.chat.services import ChatService, LLMError
from app.core.database import AsyncSessionLocal
from app.core.security import decode_access_token
from app.users.models import UserModel
from app.users.services import UserService

router = APIRouter(prefix="/chat", tags=["Chat"])

WS_UNAUTHORIZED = 4401


async def _authenticate(token: str | None) -> UserModel | None:
    if not token:
        return None
    try:
        user_id = int(decode_access_token(token))
    except (ValueError, TypeError):
        return None
    async with AsyncSessionLocal() as db:
        user = await UserService.get_by_id(db, user_id)
    if user is None or not user.is_active:
        return None
    return user


@router.websocket("/ws")
async def chat_ws(websocket: WebSocket, token: str | None = None):
    """
    Протокол (JSON):
      клиент -> {"message": str, "history": [{"role", "content"}]}
      сервер -> {"type": "start"} | {"type": "token", "content": str}
              | {"type": "sources", "sources": [{"article_id", "title"}]}
              | {"type": "done"} | {"type": "error", "detail": str}
    Токен JWT передаётся в query: /chat/ws?token=...
    """
    await websocket.accept()

    user = await _authenticate(token)
    if user is None:
        await websocket.close(code=WS_UNAUTHORIZED, reason="Not authenticated")
        return

    try:
        while True:
            raw = await websocket.receive_json()
            try:
                data = ChatClientMessage.model_validate(raw)
            except ValidationError:
                await websocket.send_json(
                    {"type": "error", "detail": "Некорректное сообщение"}
                )
                continue

            await websocket.send_json({"type": "start"})
            try:
                async with AsyncSessionLocal() as db:
                    context = await ChatService.retrieve_context(
                        db, user, data.message
                    )
                messages = ChatService.build_messages(
                    data.message, data.history, context
                )
                async for piece in ChatService.stream_completion(messages):
                    await websocket.send_json({"type": "token", "content": piece})

                sources = {a.id: a.title for a, _ in context}
                if sources:
                    await websocket.send_json(
                        {
                            "type": "sources",
                            "sources": [
                                {"article_id": i, "title": t}
                                for i, t in sources.items()
                            ],
                        }
                    )
                await websocket.send_json({"type": "done"})
            except LLMError as exc:
                await websocket.send_json({"type": "error", "detail": str(exc)})
    except (WebSocketDisconnect, ValueError):
        # ValueError — клиент прислал не-JSON
        return