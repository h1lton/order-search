from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import BaseModel


class ChatModel(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[int] = mapped_column(String(32))
    last_check_message_id: Mapped[int] = mapped_column(default=0)
