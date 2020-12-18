# Парсер ВК 
<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/Ser-guz/vk_parser">
Парсер групп в ВК с засением в БД количества участников (подписчиков) групп.<br>

## Getting Started 
1. Клонируйте в отдельную папку репозиторий:<br>
```git clone https://github.com/Ser-guz/vk_parser.git```
2. Установите зависимости:<br>
```pip install -r requirements.txt```

## Runni
1. Запустите файл `periodic.py` для создания БД.
2. В файле `periodic.py` задайте необходимое вам расписание запуска модуля `vk_parser`.
Вам может потребоваться следующая [документация](https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#crontab-schedules).<br>
```"schedule": crontab(hour=0, minute=0)```<br>
3. В консоли запустите celery beat:<br>
```celery -A periodic beat --loglevel=info```
4. Создайте 2-ю консоль и там запустите celery worker:<br>
```celery -A periodic worker --loglevel=info```

### Добавление групп ВК
При необходимости можно изменить (добавить, удалить) группы ВК.<br>
Для этого в файле `settings.ini` отредактируейте строку *group_ids*:<br>
```group_ids = <name_group1>,<name_group2>...```<br>
Обратите внимание, что разделять имена групп должен символ `,` без пробела.

### Полезная информация
Эта информация поможет во внедрении celery cron в код своего парсера:
- https://medium.com/the-andela-way/asynchronous-processing-in-celery-79f88fa599a5
- https://medium.com/the-andela-way/timed-periodic-tasks-in-celery-58c99ecf3f80
