from celery import Celery
import requests
from celery.schedules import crontab
import sqlite3
from configparser import ConfigParser
from exceptions import TakeGroupInfoException

"""Создание приложения 'periodic' с брокером сообщений RabbitMQ"""
app = Celery('periodic', broker="pyamqp://guest@localhost//")

"""Отключение службы часовых поясов для возможности использовать Celery местное время"""
app.conf.enable_utc = False


@app.task
def take_group_info():
    """Получение ответа от VK_API, экстрация из него суммарного числа участников групп ВК
    и внесение этих данных в БД"""

    config = ConfigParser()
    config.read("settings.ini")
    token = config.get("VK_API", "token")
    version = config.get("VK_API", "version")
    url = config.get("VK_API", "url")
    group_ids = "".join(config.get("VK_API", "group_ids"))
    fields = "".join(config.get("VK_API", "fields"))

    """Получение ответа от VK_API"""
    response = requests.get(url,
                            params={
                                'access_token': token,
                                'v': version,
                                'group_ids': group_ids,
                                'fields': fields
                            })

    """Перехват исключений"""
    if response.status_code != 200:
        raise TakeGroupInfoException(f"Response has unexcepted status code: {response.status_code}")
    if not response.json()['response']:
        raise TakeGroupInfoException("Response has no dict 'response'.")

    """Экстракция данных из объекта response и подготовка их к внесению в БД"""
    data = response.json()['response']
    history_record = [(item['name'], item['members_count']) for item in data]
    list_groups = [(item['name'],) for item in data]

    """Соединение с БД"""
    conn = sqlite3.connect("db_parser.db")
    cursor = conn.cursor()

    """Наполнение БД"""
    cursor.executemany("INSERT OR IGNORE INTO group_vk (name) VALUES (?)", list_groups)
    cursor.executemany("INSERT OR IGNORE INTO history_record (name, members_count) VALUES (?, ?)", history_record)

    """Применение внесенных изменений в БД и закрытие БД"""
    conn.commit()
    conn.close()


def init_db():
    """Создание БД"""
    conn = sqlite3.connect("db_parser.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS group_vk 
                          (name TEXT PRIMARY KEY,
                          created_db TIMESTAMP DEFAULT (datetime('now','localtime')))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS history_record 
                          (name TEXT,
                          members_count INT,
                          created_db TIMESTAMP DEFAULT (datetime('now','localtime')))""")
    conn.commit()
    conn.close()

app.conf.beat_schedule = {
    "take_group_info-in-onetime-everyday-task": {
        "task": "periodic.take_group_info",
        "schedule": crontab(hour=9, minute=13)
    }
}

if __name__ == '__main__':
    init_db()

