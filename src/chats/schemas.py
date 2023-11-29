from pydantic import BaseModel, ConfigDict


class ChatScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    last_check_message_id: int
