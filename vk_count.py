import sqlite3
from datetime import datetime
import requests

group_ids = 'rambler,ramblermail,horoscopesrambler,championat,championat.auto,championat_cybersport,livejournal,afisha'


def take_group_count(groups):
    token = '04cf9b5504cf9b5504cf9b555904bce3f2004cf04cf9b555bf94a8988d11539a4dcaea2'
    version = 5.92
    fields = 'members_count'

    response = requests.get('https://api.vk.com/method/groups.getById',
                            params={
                                'access_token': token,
                                'v': version,
                                'group_ids': groups,
                                'fields': fields
                            })

    date = response.json()['response']
    list_counts = [item['members_count'] for item in date]
    _total_count = sum(list_counts)
    _list_group = [(item['name'], item['members_count']) for item in date]
    return _list_group, _total_count

list_group = take_group_count(group_ids)[0]
total_count = take_group_count(group_ids)[1]

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