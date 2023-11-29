from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .parsers import parser
from src.database import get_async_session
from src.posts.schemas import PostScheme

router = APIRouter()


@router.get('/start')
async def start_parse(
    session: AsyncSession = Depends(get_async_session)
) -> list[PostScheme]:
    posts = await parser(session)
    return posts
