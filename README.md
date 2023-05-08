# kazback_reminder
Telegram-bot kazbask_reminder. Accepts a request, a time, and an event to be reminded of. Before the event, this bot sends messages to all event participants, in a private message or in a public group.


Собрать образ.
```
docker build -t letters_bot .
```

Запуск контейнера, чтоб он делал запросы на локальную машину
```
docker run --network=host --name letters_bot -p 8080:8080 -d letters_bot
```
