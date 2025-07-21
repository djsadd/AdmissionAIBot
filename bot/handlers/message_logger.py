from aiogram import Router, types, F
from db.database import async_session
from db.models import MessageModel

router = Router()


@router.message(F.text)
async def log_and_save_message(message: types.Message):
    print(message.text)
    async with async_session() as session:
        msg = MessageModel(
            user_id=message.from_user.id,
            username=message.from_user.username,
            text=message.text
        )
        session.add(msg)
        await session.commit()
@router.callback_query()
async def log_callback(callback: types.CallbackQuery):
    async with async_session() as session:
        msg = MessageModel(
            user_id=callback.from_user.id,
            username=callback.from_user.username,
            text=f"[callback] {callback.data}"
        )
        session.add(msg)
        await session.commit()
    await callback.answer()  # обязательно