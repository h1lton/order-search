import logging

from fastapi import APIRouter, Depends
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.posts.schemas import PostScheme
from src.posts.service import get_page_posts, get_post as _get_post

router = APIRouter()


@router.get("/")
async def get_posts(
        session: AsyncSession = Depends(get_async_session),
        page: int = 1
) -> list[PostScheme]:
    posts = await get_page_posts(session, page=page)
    return posts


@router.get("/{post_id}")
async def get_post(
        post_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> PostScheme:
    posts = await _get_post(session, post_id)
    return posts
