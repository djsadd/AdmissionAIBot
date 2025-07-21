from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import asyncio

from handlers import common, menu_router, ai_handler, message_logger
from handlers.documents import hanlders
from handlers.unt import handlers_unt
from db.database import init_db
from middlewares.logging import LoggingMiddleware

import os
from dotenv import load_dotenv

load_dotenv()


async def main():
    await init_db()

    bot = Bot(
        token=os.getenv("TELEGRAM_BOT_TOKEN"),
    )

    dp = Dispatcher()
    dp.include_routers(
        common.router,
        menu_router.router,
        ai_handler.router,
        hanlders.router,
        handlers_unt.router,
        message_logger.router,  # Добавляем логгер в роутеры
    )

    await bot.delete_webhook(drop_pending_updates=True)
    dp.message.middleware(LoggingMiddleware())
    dp.callback_query.middleware(LoggingMiddleware())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

# uvicorn bot.server.server:app --reload