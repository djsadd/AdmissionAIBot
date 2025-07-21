
from db.database import async_session
from db.models import ChatHistory
from sqlalchemy import select


async def save_chat_history(session_id: str, query: str, response: str, platform: str):
    async with async_session() as session:
        async with session.begin():
            history_entry = ChatHistory(
                session_id=session_id,
                query=query,
                response=response,
                platform="Telegram",
            )
            session.add(history_entry)
            # Можно получить ID (если нужно)
            await session.flush()
            return history_entry.id  # Если нужно вернуть


async def get_history_text_by_session(session_id: str) -> str:
    async with async_session() as session:
        result = await session.execute(
            select(ChatHistory).where(ChatHistory.session_id == session_id)
        )
        entries = result.scalars().all()

        if not entries:
            return "История пуста."

        formatted_history = ""
        for entry in entries:
            formatted_history += f"User: {entry.query}\nAI: {entry.response}\n\n"

        return formatted_history.strip()
