import shlex

import prompt

from primitive_db import core, utils

META_PATH = "db_meta.json"


def welcome():
    print("***")
    print("Функции:")
    print("<command> exit - выйти из программы")
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
                    print(f'- "{table_name}".')
            case "create_table":
                if args[1] is None:
                    print("Введите имя таблицы, некорректная команда.")
                else:
                    meta = core.create_table(meta, args[1], args[2:])
                    utils.save_metadata(META_PATH, meta)
            case "drop_table":
                if args[1] is None:
                    print("Введите имя таблицы, некорректная команда.")
                else:
                    meta = core.drop_table(meta, args[1])
                    utils.save_metadata(META_PATH, meta)
            case _:
                print(f'«Функции {cmd} нет.Попробуйте снова.»')

    # src/primitive_db/engine.py
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
