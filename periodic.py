from celery import Celery
import requests
from celery.schedules import crontab
from datetime import datetime
import sqlite3
from configparser import ConfigParser



"""Создание приложения 'periodic' с брокером сообщений RebbitMQ"""
app = Celery('periodic', broker="pyamqp://guest@localhost//")
"""Отключение службы часовых поясов для возможности использовать Celery местное время"""
app.conf.enable_utc = False

@app.task
def take_group_count():
    config = ConfigParser()
    config.read("settings.ini")
    token = config.get("VK_API", "token")
    version = config.get("VK_API", "version")
    url = config.get("VK_API", "url")
    group_ids = "".join(config.get("VK_API", "group_ids"))
    fields = 'members_count'

    """Получение ответа от VK_API"""
    response = requests.get(url,
                            params={
                                'access_token': token,
                                'v': version,
                                'group_ids': group_ids,
                                'fields': fields
                            })

    """Экстракция данных из объекта response и подготовка их к внесению в БД"""
    date = response.json()['response']
    list_counts = [item['members_count'] for item in date]
    total_count = sum(list_counts)
    history_record = [(group_ids, total_count)]
    list_group = [(group_ids, str(datetime.now()))]

    """Соединение с БД"""
    conn = sqlite3.connect("db_parser.db")
    cursor = conn.cursor()

    """Создание БД"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS group_vk 
                      (name TEXT PRIMARY KEY,
                      created_db TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS history_record 
                      (group_name TEXT,
                      members_count INT,
                      created_db TIMESTAMP DEFAULT (datetime('now','localtime')))""")

    """Наполнение БД"""
    cursor.executemany("INSERT OR IGNORE INTO group_vk VALUES (?, ?)", list_group)
    cursor.executemany("INSERT OR IGNORE INTO history_record (group_name, members_count) VALUES (?, ?)", history_record)

    """Применение внесенных изменений в БД и закрытие БД"""
    conn.commit()
    conn.close()


app.conf.beat_schedule = {
    "total_count-in-onetime-everyday-task": {
        "task": "periodic.take_group_count",
        "schedule": crontab(hour=22, minute=0)
    }
}

