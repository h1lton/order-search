from sqlalchemy.ext.asyncio import AsyncSession
from telethon.events import NewMessage
from telethon.tl.patched import Message

from src.chats.models import ChatModel
from src.chats.service import get_chats, update_last_check_message_id
from src.database import async_session_maker
from src.logger import logger
from src.parser.checks import check_message
from src.parser.client import client
from src.parser.parsers import parser, message_parser
from src.posts.service import create_post


async def handler_new_message(event: NewMessage.Event):
    message = event.message
    logger.info(f"New message in {message.chat.username} \"{message.text[:30]}...\"")

    async with async_session_maker() as session:
        if check_message(message):
            post = await message_parser(message)
            await create_post(session, post)
            logger.info('Created new post')

        await update_last_check_message_id(session, message.chat_id, message.id)


async def update_handler_new_message(session: AsyncSession):
    chats = await get_chats(session)
    _update_handler_new_message(chats)


def _update_handler_new_message(chats: list[ChatModel]):
    chats_ids = [chat.id for chat in chats]
    client.remove_event_handler(handler_new_message)
    client.add_event_handler(handler_new_message, NewMessage(chats=chats_ids))


async def parser_startup():
    await client.start()
    async with async_session_maker() as session:
        chats = await get_chats(session)
        await parser(session, chats=chats)
        _update_handler_new_message(chats)


async def parser_shutdown():
    await client.disconnect()
