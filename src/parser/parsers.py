from datetime import timedelta
from time import time
from typing import Union, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from telethon.tl.patched import Message
from telethon.tl.types import User

from .checks import check_message, check_message_date
from .client import client
from .files import download_message_files
from src.chats.models import ChatModel
from src.chats.service import get_chats
from src.logger import logger
from src.posts.service import create_posts
from src.posts.models import PostModel


async def message_parser(message: Message):
    post = PostModel()

    if message.sender:
        post.user_username = message.sender.username

        if isinstance(message.sender, User):
            post.user_phone = message.sender.phone

    post.create_at = message.date
    post.content = message.text
    post.files = await download_message_files(message, return_models=True)

    return post


async def chat_parser(chat: Union[str, int], min_id: int = 0):
    parsed_msg = 0
    good_msg = 0

    posts = []

    first_message = await client.get_messages(chat)
    last_message_id = first_message[0].id

    if not len(first_message) or min_id >= last_message_id:
        logger.info(f"{chat} | Parsed - 0")
        return

    async for message in client.iter_messages(chat, min_id=min_id):
        parsed_msg += 1
        if not check_message_date(message.date):
            break
        if check_message(message):
            good_msg = 0
            post = await message_parser(message)
            posts.append(post)

    per_good = good_msg / parsed_msg * 100
    logger.info(f"{chat} | Parsed - {parsed_msg} | Good - {good_msg} | {per_good:.2f}%")

    return {
        'posts': posts,
        'last_check_message_id': last_message_id,
        'parsed_msg': parsed_msg,
        'good_msg': good_msg,
    }


async def parser(session: AsyncSession, chats: Optional[list[ChatModel]] = None) -> list[PostModel]:
    parsed_msg = 0
    good_msg = 0

    all_posts = []

    if not chats:
        chats = await get_chats(session)

    start_time = time()

    logger.info('Start parse chats.')

    for chat in chats:
        data = await chat_parser(chat.id, chat.last_check_message_id)

        if data:
            all_posts += data['posts']
            chat.last_check_message_id = data['last_check_message_id']

            parsed_msg += data['parsed_msg']
            good_msg += data['good_msg']

    end_time = time()
    execution_time = timedelta(seconds=end_time - start_time)

    if parsed_msg:
        per_good = good_msg / parsed_msg * 100
        logger.info(f"Parsed - {parsed_msg} in {execution_time} | Good - {good_msg} | {per_good:.2f}%")
    else:
        logger.info(f"Parsed - 0 in {execution_time}")

    await create_posts(session, all_posts)
    return all_posts
