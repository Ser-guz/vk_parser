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
1. Запустите файл `periodic.py` для создания БД.
2. В файле `periodic.py` задайте необходимое вам расписание запуска модуля `vk_parser`.
Вам может потребоваться следующая [документация](https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#crontab-schedules).<br>
```"schedule": crontab(hour=0, minute=0)```<br>
3. В консоли запустите celery beat:<br>
```celery -A periodic beat --loglevel=info```
4. Создайте 2-ю консоль и там запустите celery worker:<br>
```celery -A periodic worker --loglevel=info```

## Модификации
### Добавление групп ВК
При необходимости можно изменить (добивить, удалить) группы ВК.<br>
Для этого в файле `settings.ini` отредактируейте строку *group_ids*:<br>
```group_ids = <name_group1>,<name_group2>...```<br>
Обратите внимание, что разделять имена групп должен символ `,` без пробела.

### Расширение собираемой информации
Для этого в архитектуре БД предусмотрен сбор информации о всех группах ВК сразу (таблицы `group_vk` и `history_record`) и сбор информации о каждой группе ВК в отдельности (таблица `group_vk_detail`).
Для расширения собираемой информации следует незначительно изменить код модуля согласно нижеприведенной инструкции.

1. В файле `settings.ini` измените значение поля `fields`, добавив к нему необходимые вам поля или удалив лишние:
```fields = <name_field1><name_field2>...``` <br>
Список дополнительных полей и их описание можно найти в [документации VK_API](https://vk.com/dev/objects/group).
Обратите внимание, что разделять имена групп должен символ `,` без пробела.

2. В файле `periodic.py` в теле функции `init_db` добавить новые поля или удалить лишние в SQL-запросе на создание таблицы `group_vk_detail`:
```
cursor.execute("""CREATE TABLE IF NOT EXISTS group_vk_detail
                          (name TEXT PRIMARY KEY,
                          members_count INT,
                          <name_field1> TYPE,
                          <name_field2> TYPE,
                          ...
                          created_db TIMESTAMP DEFAULT (datetime('now','localtime')))""")
```
3. В тоже файле в теле функции `take_group_info` изменить число полей, из которых будет формироваться список кортежей для наполнения таблицы `group_vk_detail` в БД:
```
list_group_detail = [(item['name'], item['members_count'], item['<name_field1>'], item['...']) for item in date]
```
4. В тоже файле в теле функции `take_group_info` измените SQL-запрос в БД на наполнение таблицы `group_vk_detail`:
```
cursor.executemany("INSERT OR IGNORE INTO group_vk_detail 
                    (name, members_count, <name_field1>, ...) 
                    VALUES (?, ?, ?, ...)", 
                    list_group_detail)
```
Обратите внимание, что число полей в круглых скобках после имени таблицы должно быть равно числу символов `?` в круглых скобках после `VALUES`.


Таким же способом можно расширить наполнение таблицы `history_record`:
1. Добавить необходимые поля в переменную `fields` в файле `settings.ini`.
2. Отредактировать SQL-запрос на создание таблицы в теле функции `init_db` в файле `periodic.py`.
3. Отредактировать список `list_group` с данными для наполнения таблицы в теле функции `take_group_info` в файле `periodic.py`.
4. Отредактировать SQL-запрос в БД на наполнение таблицы.
