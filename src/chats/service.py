from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from telethon.tl.types import Channel

from src.chats.models import ChatModel
from src.chats.exceptions import not_found_exception, not_chat_exception
from src.parser.client import client as parser_client


async def add_chats(session: AsyncSession, usernames: list[str]):
    chat_models = []
    try:
        entity = await parser_client.get_entity(usernames)
    except ValueError as exp:
        raise not_found_exception(exp)

    for i, chat in enumerate(entity):
        if isinstance(chat, Channel):
            chat_models.append(ChatModel(id=chat.id, username=chat.username))

        else:
            raise not_chat_exception(usernames[i])

    session.add_all(chat_models)
    await session.commit()
    return chat_models


async def get_chat(session: AsyncSession, chat_id: int):
    return await session.get(ChatModel, chat_id)


async def delete_chat(session: AsyncSession, chat_id: int):
    query = delete(ChatModel).where(ChatModel.id == chat_id)
    await session.execute(query)
    await session.commit()


async def get_chats(session: AsyncSession):
    query = select(ChatModel)
    result = await session.execute(query)
    return result.scalars().all()


async def update_last_check_message_id(session: AsyncSession, chat_id: int, message_id: int):
    query = (
        update(ChatModel).
        where(ChatModel.id == chat_id).
        values(last_check_message_id=message_id)
    )
    await session.execute(query)
    await session.commit()
