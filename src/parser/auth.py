"""
Данный модуль запускает клиент тем самым вызывая функцию авторизации.
Запускать как скрипт те `docker-compose run fastapi python -m src.parser.auth`
"""
from .client import client


async def main():
    async with client:
        print("successfully")

if __name__ == "__main__":
    client.loop.run_until_complete(main())
