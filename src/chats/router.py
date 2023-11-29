from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.params import Param
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from telethon.errors import UsernameInvalidError

from src.chats.exceptions import UsernameInvalidException
from src.chats.schemas import ChatScheme
from src.chats.service import (
    add_chats as _add_chats,
    get_chats as _get_chats,
    get_chat as _get_chat,
    delete_chat as _delete_chat,
)
from src.database import get_async_session
from src.parser.parsers import parser
from src.parser.service import update_handler_new_message

router = APIRouter()


@router.post('/', status_code=status.HTTP_204_NO_CONTENT)
async def add_chats(
        chats: list[Annotated[str, Param(min_length=5, max_length=32)]] = Body(min_length=1),
        session: AsyncSession = Depends(get_async_session),
):
    try:
        chats = await _add_chats(session, chats)
    except UsernameInvalidError:
        raise UsernameInvalidException

    await parser(session, chats=chats)
    await update_handler_new_message(session)


@router.get('/')
async def get_chats(session: AsyncSession = Depends(get_async_session)) -> list[ChatScheme]:
    return await _get_chats(session)


@router.get('/{chat_id}')
async def get_chat(
        chat_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> ChatScheme:
    chat = await _get_chat(session, chat_id)
    if chat:
        return chat
    raise HTTPException(status_code=404, detail="Chat not found")


@router.delete('/{chat_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
        chat_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    await _delete_chat(session, chat_id)
    await update_handler_new_message(session)
