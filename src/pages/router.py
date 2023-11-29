from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from markdown import markdown
from starlette.requests import Request

from src.posts.router import get_posts

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
def post_list_view(request: Request, posts=Depends(get_posts), page: int = 1):
    for post in posts:
        post.content = markdown(post.content.replace("#", "\#"))
    return templates.TemplateResponse(
        "posts/list.html",
        {
            "request": request,
            "posts": posts,
            "paginator": {
                "previous": page - 1,
                "min": page - 3 if page - 3 > 0 else 1,
                "self": page,
                "max": page + 3,
                "next": page + 1
            }
        }
    )
