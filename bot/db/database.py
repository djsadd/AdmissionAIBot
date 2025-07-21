# bot/db/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./bot_db.sqlite"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

