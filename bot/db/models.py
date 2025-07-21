# bot/db/models.py

from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from .database import Base
from sqlalchemy import Enum
import enum
from pydantic import BaseModel


class PlatformEnum(str, enum.Enum):
    whatsapp = "Whatsapp"
    telegram = "Telegram"


class MessageModel(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    username = Column(String(100))
    text = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


class AskRequest(BaseModel):
    query: str
    uuid: str
    platform: PlatformEnum


class ChatHistory(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(256))
    query = Column(Text)
    response = Column(Text)
    platform = Column(Enum(PlatformEnum), nullable=False)

