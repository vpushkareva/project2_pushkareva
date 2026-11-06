import shlex

import prompt
from prettytable import PrettyTable

from primitive_db import core, utils

META_PATH = "db_meta.json"


def parse_condition(text, schema):
    col, value = text.split("=")
    col = col.strip()
    value = value.strip().strip('"')
    for column in schema:
        col_name, col_type = column.split(":")
        if col_name == col:
            return {col: core.convert(value, col_type)}
    return {col: value}


def print_table(schema, rows):
    table = PrettyTable()
    table.field_names = [c.split(":")[0] for c in schema]
    for row in rows:
        table.add_row([row.get(name) for name in table.field_names])
    print(table)


def welcome():
    print("***Операции с данными***")
    print()
    print("Функции:")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись.")  # noqa: E501
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.")  # noqa: E501
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.")  # noqa: E501
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.")  # noqa: E501
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация")


def run():
    welcome()
    while True:
        meta = utils.load_metadata(META_PATH)
        user_input = prompt.string(">>>Введите команду: ")
        args = shlex.split(user_input)
        cmd = args[0]
        match cmd:
            case "help":
                print_help()
            case "exit":
                break
            case "list_tables":
                for table_name in meta:
                    print(f"- {table_name}")
            case "create_table":
                if len(args) < 2:
                    print("Введите имя таблицы, некорректная команда.")
                else:
                    meta = core.create_table(meta, args[1], args[2:])
                    utils.save_metadata(META_PATH, meta)
            case "drop_table":
                if len(args) < 2:
                    print("Введите имя таблицы, некорректная команда.")
                else:
                    meta = core.drop_table(meta, args[1])
                    utils.save_metadata(META_PATH, meta)
            case "insert":
                if len(args) < 5 or args[1] != "into" or args[3] != "values":
                    print("Некорректная команда insert. Попробуйте снова.")
                elif args[2] not in meta:
                    print(f'Ошибка: Таблица "{args[2]}" не существует.')
                else:
                    table_name = args[2]
                    raw = " ".join(args[4:])
                    if not (raw.startswith("(") and raw.endswith(")")):
                        print("Значения нужно указать в скобках. Попробуйте снова.")
                        continue
                    values = [v.strip().strip('"') for v in raw[1:-1].split(",")]
                    data = utils.load_table_data(table_name)
                    data = core.insert(meta, table_name, values, data)
                    utils.save_table_data(table_name, data)
            case "select":
                if len(args) < 3 or args[1] != "from":
                    print("Некорректная команда select. Попробуйте снова.")
                elif args[2] not in meta:
                    print(f'Ошибка: Таблица "{args[2]}" не существует.')
                else:
                    table_name = args[2]
                    schema = meta[table_name]
                    data = utils.load_table_data(table_name)
                    if "where" in args:
                        where_text = " ".join(args[args.index("where") + 1:])
                        data = core.select(data, parse_condition(where_text, schema))
                    print_table(schema, data)
            case "update":
                if len(args) < 4 or "set" not in args or "where" not in args:
                    print("Некорректная команда update. Попробуйте снова.")
                elif args[1] not in meta:
                    print(f'Ошибка: Таблица "{args[1]}" не существует.')
                else:
                    table_name = args[1]
                    schema = meta[table_name]
                    set_text = " ".join(args[args.index("set") + 1:args.index("where")])
                    where_text = " ".join(args[args.index("where") + 1:])
                    data = utils.load_table_data(table_name)
                    set_clause = parse_condition(set_text, schema)
                    where_clause = parse_condition(where_text, schema)
                    data = core.update(data, set_clause, where_clause, table_name)
                    utils.save_table_data(table_name, data)
            case "delete":
                if len(args) < 4 or args[1] != "from" or args[3] != "where":
                    print("Некорректная команда delete. Попробуйте снова.")
                elif args[2] not in meta:
                    print(f'Ошибка: Таблица "{args[2]}" не существует.')
                else:
                    table_name = args[2]
                    schema = meta[table_name]
                    where_text = " ".join(args[4:])
                    data = utils.load_table_data(table_name)
                    clause = parse_condition(where_text, schema)
                    data = core.delete(data, clause, table_name)
                    utils.save_table_data(table_name, data)
            case "info":
                if len(args) < 2:
                    print("Введите имя таблицы, некорректная команда.")
                elif args[1] not in meta:
                    print(f'Ошибка: Таблица "{args[1]}" не существует.')
                else:
                    table_name = args[1]
                    count = len(utils.load_table_data(table_name))
                    print(f"Таблица: {table_name}")
                    print(f"Столбцы: {', '.join(meta[table_name])}")
                    print(f"Количество записей: {count}")
            case _:
                print(f"Функции {cmd} нет. Попробуйте снова.")

def print_help():
    """Prints the help message for the current mode."""

    print("\n***Работа с таблицами***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу")  # noqa: E501
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\n***Операции с данными***")
    print("<command> insert into <имя_таблицы> values (<значение1>, ...) - создать запись")  # noqa: E501
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи")  # noqa: E501
    print("<command> select from <имя_таблицы> - прочитать все записи")
    print("<command> update <имя_таблицы> set <столбец> = <значение> where <столбец> = <значение> - обновить запись")  # noqa: E501
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись")  # noqa: E501
    print("<command> info <имя_таблицы> - информация о таблице")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")
