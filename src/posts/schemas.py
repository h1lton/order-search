from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_serializer, ConfigDict

from src.config import settings


class FileScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    path: str


class PostScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_at: datetime
    content: str
    user_username: Optional[str]
    user_phone: Optional[str]
    files: list[FileScheme]

    @field_serializer("files")
    def serialize_url(self, files: list[FileScheme], _info) -> list[str]:
        return [settings.URL + file.path for file in files]
