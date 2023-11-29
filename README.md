<a name="readme-top"></a>
<br>
<div align="center">
  <a href="https://github.com/h1lton/order-search">
    <img src="https://img.icons8.com/?size=150&id=YrFixm78K3F0&format=png" alt="Logo">
  </a>
  <h3>Search For Orders</h3>
  <p>
    Сервис по поиску заказов
    <br>
    <a href="https://github.com/h1lton/order-search"><strong>Explore the docs »</strong></a>
    <br>
    <br>
  </p>

  <img src="https://skillicons.dev/icons?i=py,fastapi,mysql,docker&theme=light" alt="Tech">

  <p>
    <br>
    <a href="https://github.com/h1lton/order-search">View Demo</a>
    ·
    <a href="https://github.com/h1lton/order-search/issues">Report Bug</a>
    ·
    <a href="https://github.com/h1lton/order-search/issues">Request Feature</a>
  </p>
</div>


<details>
  <summary>Оглавление</summary>
  <ol>
    <li><a href="#стек-технологий">Стек технологий</a></li>
    <li><a href="#установка">Установка</a></li>
  </ol>
</details>

## Стек технологий

- <img src="https://skillicons.dev/icons?i=py&theme=light" alt="icon" style="width: 25px"> Python 3.9
- <img src="https://skillicons.dev/icons?i=fastapi&theme=light" alt="icon" style="width: 25px"> FastAPI
- <img src="https://skillicons.dev/icons?i=py&theme=light" alt="icon" style="width: 25px"> Telethon
- <img src="https://skillicons.dev/icons?i=py&theme=light" alt="icon" style="width: 25px"> Alembic
- <img src="https://skillicons.dev/icons?i=py&theme=light" alt="icon" style="width: 25px"> SQLAlchemy
- <img src="https://skillicons.dev/icons?i=mysql&theme=light" alt="icon" style="width: 25px"> MySQL
- <img src="https://skillicons.dev/icons?i=docker&theme=light" alt="icon" style="width: 25px"> Docker & Docker Compose

<p align="right">(<a href="#readme-top">вернуться наверх</a>)</p>

## Установка

1. Для начало нужно получить API_ID и API_HASH они нужны для парсера

   [my.telegram.org/auth](https://my.telegram.org/auth)

   Вставляем их в [.env](.env), заранее его нужно создать по [.env.template](.env.template)
2. Создаём образы
   ```sh
   docker-compose build
   ```
3. Запускаем скрипт для авторизации в тг
   ```sh
   docker-compose run app python -m src.parser.auth
   ```
    - Вводим номер телефона без +
    - Вводим код который пришёл в telegram
    - Если всё успешно вы увидите `successfully`
4. При первом запуске нужно проинициализировать дб.
   ```
   docker-compose up db
   ```
   Это займет какое-то время.
   ```sh
   ready for connections. Version: '8.2.0'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
   ```
   Как увидете это сообщение можете запускать app
   ```sh
   docker-compose up app
   ```

В дальнейшем просто запускайте docker-compose

```sh
docker-compose up
```

Далее можно работать с API, не забудьте взять ACCESS_TOKEN в [.env](.env)
