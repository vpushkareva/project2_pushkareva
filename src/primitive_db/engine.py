import shlex

import prompt

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


def welcome():
    print("***База данных***")
    print()
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу")  # noqa: E501
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
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
            case _:
                print(f"Функции {cmd} нет. Попробуйте снова.")

def print_help():
    """Prints the help message for the current mode."""

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")
