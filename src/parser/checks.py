from datetime import datetime
from typing import Optional

from telethon.tl.patched import Message

from src.config import settings


def check_message_text(text: Optional[str]) -> bool:
    """Проверяет текст сообщения"""
    # Это условие можно поменять на NLP
    if text and "ищ" in text.lower():
        return True
    else:
        return False


def check_message_date(date: datetime) -> bool:
    """Проверяет дату что-бы она была в пределах установленных в config"""
    if date > datetime.now(date.tzinfo) - settings.MAX_PARSED_DATETIME:
        return True
    else:
        return False


def check_message(message: Message) -> bool:
    """Проверяет сообщение на различные условия"""
    if not message.is_reply and check_message_text(message.text):
        return True
    return False
