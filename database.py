import sqlite3

conn = sqlite3.connect('db_parser.db')
cursor = conn.cursor()

"""Таблица групп ВК и количества участников в них"""
cursor.execute("""
                CREATE TABLE group_vk
                (name TEXT, members_count INT)
                """)


"""Таблица с записями о количестве участников групп в определенный момент времени
Должны быть поля о дате записи в таблицу, суммарное количество участников всех групп
Вопросы:
- какой формат столбца с датой?
- как связать столбец с суммой участников с таблицей групп ВК? 
- как провести сумму участников из таблицы групп ВК и передать это значение в таблицу?
"""
cursor.execute("""
                CREATE TABLE history_record
                (update_date TEXT, members_count INT)
                """)

conn.close()