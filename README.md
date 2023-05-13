# kazback_reminder
Telegram-bot kazbask_reminder. Accepts a request, a time, and an event to be reminded of. Before the event, this bot sends messages to all event participants, in a private message or in a public group.

Запустить локально.
```
python bot_main.py
```

Собрать образ.
```
docker build -t letters_bot .
```

Запуск контейнера, чтоб он делал запросы на локальную машину на сенвере
```
docker run --network=host --name letters_bot --rm -p 8080:8080 -d kultmet/letters_bot:1.1

это самая актуальная для ручного запуска
docker run --env TELEGRAM_TOKEN={Подставить актуальный токен бота}--network=host --name letters_bot --rm -p 8080:8080 -d kultmet/letters_bot:1.1

```


Сделано:
    интерфейсы:
        для получения всех скиллов пользователя
        для добавления скилла в стэк пользователя
    API:
        для получения списка скиллов
        для добавления скилла
    Удаление сообщений скрипта, - "Написание письма"
    поменял эндпоинт требований

Задачи 
    Сделать CD (автодеплой)
