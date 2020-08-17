from celery import Celery
import requests
from celery.schedules import crontab
from datetime import datetime
import sqlite3

"""Создание приложения 'periodic' с брокером сообщений RebbitMQ"""
app = Celery('periodic', broker="pyamqp://guest@localhost//")
"""Отключение службы часовых поясов для возможности использовать Celery местное время"""
app.conf.enable_utc = False

@app.task
def take_group_count():
    token = '04cf9b5504cf9b5504cf9b555904bce3f2004cf04cf9b555bf94a8988d11539a4dcaea2'
    version = 5.92
    fields = 'members_count'
    group_ids = 'rambler,ramblermail,horoscopesrambler,championat,championat.auto,championat_cybersport,livejournal,afisha'

    response = requests.get('https://api.vk.com/method/groups.getById',
                            params={
                                'access_token': token,
                                'v': version,
                                'group_ids': group_ids,
                                'fields': fields
                            })

    date = response.json()['response']
    list_counts = [item['members_count'] for item in date]
    _total_count = sum(list_counts)
    _list_group = [(item['name'], item['members_count']) for item in date]
    return _list_group, _total_count


list_group = take_group_count()[0]
total_count = take_group_count()[1]

@app.task
def insert_to_db():
    conn = sqlite3.connect("db_parser.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM group_vk")
    cursor.executemany("INSERT INTO group_vk VALUES (?, ?)", list_group)

    update_date = str(datetime.now())
    history_record = [(update_date, total_count)]
    cursor.executemany("INSERT INTO history_record VALUES (?, ?)", history_record)

    conn.commit()
    conn.close()

app.conf.beat_schedule = {
    "insert_to_db-in-onetime-everyday-task": {
        "task": "periodic.insert_to_db",
        "schedule": crontab(hour=8, minute="32")
    },
    "total_count-in-ten-seconds-task": {
        "task": "periodic.take_group_count",
        "schedule": crontab(hour=8, minute="31")
    }
}

