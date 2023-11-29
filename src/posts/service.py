from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload

from src.posts.models import PostModel, FileModel


async def create_post(session: AsyncSession, post: PostModel):
    session.add(post)
    await session.commit()
    return post


async def create_posts(session: AsyncSession, posts: list[PostModel]):
    session.add_all(posts)
    await session.commit()
    return posts


async def get_post(session: AsyncSession, post_id: int):
    query = select(PostModel).where(PostModel.id == post_id)
    result = await session.execute(query)
    return result


async def get_posts(session: AsyncSession, limit: int = 20, offset: int = 0):
    query = (
        select(PostModel)
        .order_by(PostModel.create_at.desc())
        .limit(limit)
        .offset(offset)
        .options(subqueryload(PostModel.files))
    )
    result = await session.execute(query)
    return result.scalars().all()


async def get_page_posts(session: AsyncSession, page: int):
    return await get_posts(session, offset=20 * (page - 1))
