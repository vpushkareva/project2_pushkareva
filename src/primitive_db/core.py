from primitive_db.constants import ID_COLUMN, VALID_TYPES
from primitive_db.decorators import confirm_action, handle_db_errors, log_time


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создаёт таблицу со столбцом ID:int первым, проверяет типы и дубликаты."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    for col in columns:
        parts = col.split(":")
        if len(parts) != 2 or parts[1] not in VALID_TYPES:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata

    cols = [ID_COLUMN] + columns
    metadata[table_name] = cols
    print(f'Таблица "{table_name}" успешно создана со столбцами: {", ".join(cols)}')
    return metadata


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """Удаляет таблицу из метаданных, спросив подтверждение."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata

    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


@handle_db_errors
@log_time
def insert(metadata, table_name, values, table_data):
    """Добавляет запись с автогенерированным ID, проверяя количество и типы."""
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


@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    """Возвращает все записи или только совпадающие с условием."""
    if where_clause is None:
        return table_data
    col, value = list(where_clause.items())[0]
    return [r for r in table_data if r.get(col) == value]


@handle_db_errors
@confirm_action("удаление записи")
def delete(table_data, where_clause, table_name):
    """Удаляет записи по условию, спросив подтверждение."""
    if where_clause is None:
        return table_data
    col, value = list(where_clause.items())[0]
    found = [r for r in table_data if r.get(col) == value]
    if not found:
        print("Записи по условию не найдены.")
        return table_data
    for r in found:
        print(f'Запись с ID={r["ID"]} успешно удалена из таблицы "{table_name}".')
    return [r for r in table_data if r.get(col) != value]


@handle_db_errors
def update(table_data, set_clause, where_clause, table_name):
    """Обновляет поля записей, найденных по условию."""
    where_col, where_value = list(where_clause.items())[0]
    set_col, set_value = list(set_clause.items())[0]

    found = [r for r in table_data if r.get(where_col) == where_value]
    if not found:
        print("Записи по условию не найдены.")
        return table_data
    for r in found:
        r[set_col] = set_value
        print(f'Запись с ID={r["ID"]} в таблице "{table_name}" успешно обновлена.')
    return table_data


def convert(value, col_type):
    """Приводит строковое значение к типу столбца: int, bool или str."""
    if col_type == "int":
        return int(value)
    if col_type == "bool":
        return value == "true"
    return value