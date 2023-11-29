from telethon import TelegramClient

from src.config import settings

client = TelegramClient(
    'parser',
    settings.API_ID,
    settings.API_HASH,
    system_version='4.16.30-vxCUSTOM'
)
