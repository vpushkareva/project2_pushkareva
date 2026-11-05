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