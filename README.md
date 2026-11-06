# project2_pushkareva

Учебный проект №2 курса: примитивная база данных прямо в консоли.
Пакет называется primitive_db, после установки запускается командой database.

Всё хранится в JSON-файлах: описания таблиц — в db_meta.json, данные каждой таблицы — в data/<имя>.json. Перезапустил программу — данные на месте.

## Запуск

Нужен [uv](https://docs.astral.sh/uv/). Потом две команды:

    uv sync
    uv run database

## Управление таблицами

    create_table users name:str age:int is_active:bool   — создать таблицу
    list_tables                                          — список таблиц
    drop_table users                                     — удалить таблицу

Столбец ID:int добавляется сам, задавать его не нужно. Типы: int, str, bool.

## Операции с записями

    insert into users values ("Sergei", 28, true)    — добавить запись
    select from users                                — показать все записи
    select from users where age = 28                 — показать по условию
    update users set age = 29 where name = "Sergei"  — обновить запись
    delete from users where ID = 1                   — удалить запись
    info users                                       — что за таблица и сколько записей
    help                                             — справка
    exit                                             — выход

Строки пишутся в кавычках, true/false — это bool, ID программа придумывает сама.

## Надёжность

- Опасные операции (удаление таблицы, удаление записи) сначала спрашивают подтверждение: `y` — выполнить, любой другой ответ — отмена.
- Ошибки не роняют программу: неверные значения, несуществующие таблицы и файлы обрабатываются с понятным сообщением.
- Одинаковые запросы select кэшируются — повторный ответ мгновенный. После любого изменения данных кэш сбрасывается.
- insert и select показывают время выполнения.

## Демонстрация

[![asciicast](https://asciinema.org/a/XYZNWOESEyuGJ9MU.svg)](https://asciinema.org/a/XYZNWOESEyuGJ9MU)
