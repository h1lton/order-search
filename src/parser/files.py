import string
from random import choices
from typing import Union, Optional

from telethon.tl.patched import Message

from src.posts.models import FileModel

characters = string.ascii_lowercase + string.digits


def random_string(length) -> str:
    return ''.join(choices(characters, k=length))


def random_path() -> str:
    return f"files/{random_string(2)}/{random_string(2)}/{random_string(10)}"


async def get_media_messages(original_message: Message, max_amp=10) -> list[Message]:
    """

    :param original_message:
    :param max_amp: максимальное кол-во media в media group
    :return: список сообщений media group
    """
    if original_message.grouped_id is None:
        return [original_message] if original_message.media is not None else []

    messages = await original_message.client.get_messages(
        original_message.chat_id,
        min_id=original_message.id - max_amp,
        max_id=original_message.id + max_amp
    )
    files = []
    for message in messages:
        if (
            message is not None
            and message.grouped_id == original_message.grouped_id
            and message.media is not None
        ):
            files.append(message)
    return files


async def download_file(message: Message) -> Optional[str]:
    path = await message.download_media(file=random_path())
    return path


async def download_message_files(
        original_message: Message,
        return_models: bool = False
) -> list[Union[str, FileModel]]:
    """
    Скачивает все файлы прикрепленные к сообщению
    и возвращает список FileModels или список путей
    """
    list_messages = await get_media_messages(original_message)
    path_list = []

    for message in list_messages:
        path = await download_file(message)
        if path:
            if return_models:
                path_list.append(FileModel(path=path))
            else:
                path_list.append(path)

    return path_list
