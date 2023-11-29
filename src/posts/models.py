from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import BaseModel


class PostModel(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    create_at: Mapped[datetime]
    content: Mapped[str] = mapped_column(String(5000))
    user_username: Mapped[Optional[str]] = mapped_column(String(32))
    user_phone: Mapped[Optional[str]] = mapped_column(String(15))

    files: Mapped[list["FileModel"]] = relationship(back_populates="post")


class FileModel(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    path: Mapped[str] = mapped_column(String(100))

    post: Mapped["PostModel"] = relationship(back_populates="files")
