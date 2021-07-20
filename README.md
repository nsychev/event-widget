# Виджет для регистрации на события

Позволяет регистрировать пользователей на событие через Telegram.

![Пример записи](https://i.imgur.com/7J32wze.png)

## Как пользоваться

Создайте файл `config/config.yaml` с конфигурацией. Пример файла:

```yaml
SECRET_KEY: 1234567890abcdef
TELEGRAM:
    token: 123456789:ABCDEFGHIJKLMNOPQRSTUVW_xyz_1234567
    username: ct_abit_bot
DATABASE_URL: postgresql://coffee:ilikecoffee@db:5432/coffee
SESSION_COOKIE_NAME: coffee_session
SESSION_COOKIE_SECURE: True
SESSION_COOKIE_HTTPONLY: True
ADMIN_CREDENTIALS: base64(login:password)
```

Запустите Docker:

```bash
docker-compose up -d
```

Создайте мероприятие и слоты в базе данных.

## Лицензия

[MIT](LICENSE)
