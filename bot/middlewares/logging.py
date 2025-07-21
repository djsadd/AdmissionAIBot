from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable
from db.database import async_session
from db.models import MessageModel
from datetime import datetime


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        try:
            if isinstance(event, Message):
                text = event.text or "[non-text message]"
                user_id = event.from_user.id
                username = event.from_user.username
            elif isinstance(event, CallbackQuery):
                text = f"[callback] {event.data}"
                user_id = event.from_user.id
                username = event.from_user.username
            else:
                return await handler(event, data)  # Неизвестный тип — пропускаем

            async with async_session() as session:
                msg = MessageModel(
                    user_id=user_id,
                    username=username,
                    text=text,
                    timestamp=datetime.utcnow()
                )
                session.add(msg)
                await session.commit()

        except Exception as e:
            print(f"[LoggingMiddleware Error] {e}")

        return await handler(event, data)
