import sqlite3
from configparser import ConfigParser
from datetime import datetime
import requests


def take_group_count():
    config = ConfigParser()
    config.read("settings.ini")
    token = config.get("VK_API", "token")
    version = config.getfloat("VK_API", "version")
    url = config.get("VK_API", "url")
    fields = 'members_count'
    groups = "".join(config.get("VK_API", "group_ids"))

    response = requests.get(url,
                            params={
                                'access_token': token,
                                'v': version,
                                'group_ids': groups,
                                'fields': fields
                            })
    date = response.json()['response']
    list_counts = [item['members_count'] for item in date]
    total_count = sum(list_counts)
    list_group = [item['name'] for item in date]
    history_record = [(str(datetime.now()), total_count)]
    group = tuple(groups,)
    qw = groups.partition('12345')
    qwe = []


    print(1)


list_group, total_count = take_group_count()

conn = sqlite3.connect("db_parser.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM group_vk")
cursor.executemany("INSERT INTO group_vk VALUES (?, ?)", list_group)

update_date = str(datetime.now())
history_record = [(update_date, total_count)]
cursor.executemany("INSERT INTO history_record VALUES (?, ?)", history_record)

conn.commit()
conn.close()

# print(take_group_count(group_ids)[1])
# print(total_count)