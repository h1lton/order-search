from fastapi import FastAPI, Depends, APIRouter
from starlette.staticfiles import StaticFiles

from .chats.router import router as chats_router
from .pages.router import router as pages_router
from .parser.router import router as parser_router
from .parser.service import parser_startup, parser_shutdown
from .posts.router import router as posts_router

from .security import access_check

app = FastAPI()


app.mount("/files", StaticFiles(directory="files"), name="files")
app.mount("/static", StaticFiles(directory="static"), name="static")

api_router = APIRouter()

api_router.include_router(
    chats_router,
    prefix="/chats",
    tags=["Chats"],
    dependencies=[Depends(access_check)],
)
api_router.include_router(
    parser_router,
    prefix="/parser",
    tags=["Parser"],
    dependencies=[Depends(access_check)]
)
api_router.include_router(
    posts_router,
    prefix="/posts",
    tags=["Posts"],
)

app.include_router(
    api_router,
    prefix="/api/v1",
)

app.include_router(
    pages_router,
    tags=["Pages"]
)


@app.on_event("startup")
async def startup_event():
    await parser_startup()


@app.on_event("shutdown")
async def shutdown_event():
    await parser_shutdown()
