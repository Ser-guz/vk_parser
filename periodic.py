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
def take_group_info():
    """Получение ответа от VK_API, экстрация из него суммарного числа участников групп ВК
    и внесение этих данных в БД>"""

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

    """Экстракция данных из объекта response и подготовка их к внесению в БД"""
    date = response.json()['response']
    list_counts = [item['members_count'] for item in date]
    total_count = sum(list_counts)
    history_record = [(group_ids, total_count)]
    list_group = [(group_ids, str(datetime.now()))]
    list_group_detail = [(item['name'], item['members_count']) for item in date]

    """Соединение с БД"""
    conn = sqlite3.connect("db_parser.db")
    cursor = conn.cursor()

    """Наполнение БД"""
    cursor.executemany("INSERT OR IGNORE INTO group_vk VALUES (?, ?)", list_group)
    cursor.executemany("INSERT OR IGNORE INTO history_record (group_name, members_count) VALUES (?, ?)", history_record)
    cursor.executemany("INSERT OR IGNORE INTO group_vk_detail (name, members_count) VALUES (?, ?)", list_group_detail)

    """Применение внесенных изменений в БД и закрытие БД"""
    conn.commit()
    conn.close()

def init_db():
    """Создание БД"""
    conn = sqlite3.connect("db_parser.db")
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS group_vk 
                          (name TEXT PRIMARY KEY,
                          created_db TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS history_record 
                          (group_name TEXT,
                          members_count INT,
                          created_db TIMESTAMP DEFAULT (datetime('now','localtime')))""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS group_vk_detail
                          (name TEXT PRIMARY KEY,
                          members_count INT,
                          created_db TIMESTAMP DEFAULT (datetime('now','localtime')))""")
    conn.commit()
    conn.close()

app.conf.beat_schedule = {
    "take_group_info-in-onetime-everyday-task": {
        "task": "periodic.take_group_info",
        "schedule": crontab(hour=10, minute=44)
    }
}

if __name__ == '__main__':
    init_db()

