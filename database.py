import sqlite3

conn = sqlite3.connect('db_parser.db')
cursor = conn.cursor()

# """Таблица групп ВК и количества участников в них"""
# cursor.execute("""
#                 CREATE TABLE group_vk
#                 (name TEXT, members_count INT)
#                 """)

cursor.execute("""
                DELETE FROM group_vk
                """)


# """Таблица с записями о количестве участников групп в определенный момент времени.
# Должны быть поля о дате записи в таблицу, суммарное количество участников всех групп."""
# cursor.execute("""
#                 CREATE TABLE history_record
#                 (update_date TEXT, members_count INT)
#                 """)

cursor.execute("""
                DELETE FROM history_record
                """)
conn.commit()
conn.close()