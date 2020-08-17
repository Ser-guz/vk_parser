# Парсер ВК 
<img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/Ser-guz/vk_parser">
Парсер групп в ВК с внесением в БД суммарного количества участников (подписчиков) групп.<br>

## Getting Started 
1. Клонируйте в отдельную папку репозиторий:<br>
```git clone https://github.com/Ser-guz/vk_parser.git```
2. Установите зависимости:<br>
```pip install -r requirements.txt```

## Running the test
Запустите тест

## Runnig
1. В файле `periodic.py` задайте необходимое вам расписание запуска модуля `vk_parser`.
Вам может потребоваться [документация](https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#crontab-schedules).<br>
```"schedule": crontab(hour=0, minute=0)```<br>
2. В консоли запустите celery beat:<br>
```celery -A periodic beat --loglevel=info```
3. Создайте 2-ю консоль и там запустите celery worker:<br>
```celery -A periodic worker --loglevel=info```
