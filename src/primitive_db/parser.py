from primitive_db import core


def parse_condition(text, schema):
    """Разбирает условие вида "age = 28" в словарь, приводя значение по схеме."""
    col, value = text.split("=")
    col = col.strip()
    value = value.strip().strip('"')
    for column in schema:
        col_name, col_type = column.split(":")
        if col_name == col:
            return {col: core.convert(value, col_type)}
    return {col: value}


def parse_values(raw):
    """Разбирает хвост values (...): срезает скобки и режет значения по запятым."""
    return [v.strip().strip('"') for v in raw[1:-1].split(",")]
