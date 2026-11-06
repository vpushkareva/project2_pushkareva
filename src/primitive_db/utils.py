import json
import os


def load_metadata(filepath):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data


def save_metadata(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def load_table_data(table_name):
    try:
        with open(f"data/{table_name}.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    return data


def save_table_data(table_name, data):
    os.makedirs("data", exist_ok=True)
    with open(f"data/{table_name}.json", "w") as f:
        json.dump(data, f, indent=2)