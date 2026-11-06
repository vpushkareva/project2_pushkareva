ALLOWED_TYPES = {"int", "str", "bool"}


def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    for col in columns:
        parts = col.split(":")
        if len(parts) != 2 or parts[1] not in ALLOWED_TYPES:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata

    cols = ["ID:int"] + columns
    metadata[table_name] = cols
    print(f'Таблица "{table_name}" успешно создана со столбцами: {", ".join(cols)}')
    return metadata


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def insert(metadata, table_name, values, table_data):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return table_data

    schema = metadata[table_name]
    user_columns = schema[1:]

    if len(values) != len(user_columns):
        print("Некорректное количество значений. Попробуйте снова.")
        return table_data

    record = {}
    for i, col in enumerate(user_columns):
        col_name, col_type = col.split(":")
        record[col_name] = convert(values[i], col_type)

    if table_data:
        new_id = max(r["ID"] for r in table_data) + 1
    else:
        new_id = 1
    record["ID"] = new_id

    table_data.append(record)
    print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')
    return table_data


def select(table_data, where_clause=None):
    if where_clause is None:
        return table_data
    col, value = list(where_clause.items())[0]
    return [r for r in table_data if r.get(col) == value]


def delete(table_data, where_clause, table_name):
    if where_clause is None:
        return table_data
    col, value = list(where_clause.items())[0]
    found = [r for r in table_data if r.get(col) == value]
    for r in found:
        print(f'Запись с ID={r["ID"]} успешно удалена из таблицы "{table_name}".')
    return [r for r in table_data if r.get(col) != value]


def update(table_data, set_clause, where_clause, table_name):
    where_col, where_value = list(where_clause.items())[0]
    set_col, set_value = list(set_clause.items())[0]

    found = [r for r in table_data if r.get(where_col) == where_value]
    for r in found:
        r[set_col] = set_value
        print(f'Запись с ID={r["ID"]} в таблице "{table_name}" успешно обновлена.')
    return table_data


def convert(value, col_type):
    if col_type == "int":
        return int(value)
    if col_type == "bool":
        return value == "true"
    return value