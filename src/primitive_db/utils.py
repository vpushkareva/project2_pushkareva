import json
import os

from primitive_db.constants import DATA_DIR


def load_metadata(filepath):
    """Читает метаданные таблиц из JSON-файла, нет файла — пустой словарь."""
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data


def save_metadata(filepath, data):
    """Сохраняет метаданные таблиц в JSON-файл."""
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def load_table_data(table_name):
    """Читает записи таблицы из data/<имя>.json, нет файла — пустой список."""
    try:
        with open(f"{DATA_DIR}/{table_name}.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    return data


def save_table_data(table_name, data):
    """Сохраняет записи таблицы в data/<имя>.json, создав папку при необходимости."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(f"{DATA_DIR}/{table_name}.json", "w") as f:
        json.dump(data, f, indent=2)
