from sqlalchemy import and_, or_

def parse_filter_expression(field, value, model):
    parts = field.split("__")
    column_name = parts[0]
    operator = parts[1] if len(parts) > 1 else "eq"

    column = getattr(model, column_name, None)
    if not column:
        return None

    if operator == "eq":
        return column == value
    elif operator == "contains":
        return column.ilike(f"%{value}%")
    elif operator == "startswith":
        return column.ilike(f"{value}%")
    elif operator == "gt":
        return column > value
    elif operator == "lt":
        return column < value
    elif operator == "in":
        return column.in_(value.split(","))
    return None
