- Для начало нужно получить API_ID и API_HASH [тут](https://my.telegram.org/auth), вставляем их в `.env`,
они нужены для парсера
- Создаём образы `docker-compose build`
- Запускаем скрипт для авторизации в тг `docker-compose run fastapi python -m src.parser.auth`
- Вводим номер телефона без +
- Вводим код который пришёл в telegram
- Если всё успешно вы увидите `successfully`
- При первом запуске нужно проинициализировать дб,
поэтому что бы не вызывать ошибок в приложении запустите контейнер db
`docker-compose up db`, это займет какое то время

```sh
ready for connections. Version: '8.2.0'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server - GPL.
```

- как увидете это сообщение можете запускать fastapi `docker-compose up fastapi`
- В дальнейшем запускайте контейнеры `docker-compose up`
- Далее можно работать с api, не забудьте взять ACCESS_TOKEN в `.env`
- Если что чаты добавляются по username чата, при добавлении прогружаются последние сообщения за неделю и загружаются в дб,
и после 204 response можете смотреть по http://127.0.0.1:8000/api/v1/posts/
или по http://127.0.0.1:8000/