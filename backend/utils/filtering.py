from datetime import datetime, date
from sqlalchemy import and_, or_
from fastapi import HTTPException

# If True: field=value on TEXT columns becomes ILIKE %value%
# If False: field=value remains exact match
DEFAULT_FUZZY_STRINGS = False

def _get_col(model, column_name):
    col = getattr(model, column_name, None)
    if col is None:
        return None
    # crude guard: should have .type
    if not hasattr(col, "type"):
        return None
    return col

def _col_type_name(col):
    return getattr(getattr(col, "type", None), "__class__", type(None)).__name__

def _to_bool(v: str) -> bool:
    s = str(v).strip().lower()
    if s in {"true", "1", "yes", "y"}:
        return True
    if s in {"false", "0", "no", "n"}:
        return False
    raise HTTPException(status_code=400, detail=f"Invalid boolean: {v}")

def _cast_scalar(raw: str, col):
    t = _col_type_name(col)
    if t in {"Integer"}:
        return int(raw)
    if t in {"Float", "Numeric", "DECIMAL"}:
        return float(raw)
    if t in {"Boolean"}:
        return _to_bool(raw)
    if t in {"Date"}:
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid date (YYYY-MM-DD): {raw}")
    if t in {"DateTime"}:
        try:
            # ISO8601
            return datetime.fromisoformat(raw)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid datetime (ISO8601): {raw}")
    # default: treat as string
    return raw

def _cast_list(raw_csv: str, col):
    parts = [p.strip() for p in (raw_csv or "").split(",") if p.strip() != ""]
    if not parts:
        raise HTTPException(status_code=400, detail="Empty list for __in operator")
    return [_cast_scalar(p, col) for p in parts]

def parse_filter_expression(field, value, model):
    """
    Supports:
      eq (default), contains, startswith, endswith,
      gt, lt, gte, lte, in

    Example:
      name__contains=abc
      price__gt=100
      vendor_id__in=1,2,3
      active=true
    """
    parts = field.split("__")
    column_name = parts[0]
    operator = parts[1].lower() if len(parts) > 1 else "eq"

    col = _get_col(model, column_name)
    if not col:
        return None

    t = _col_type_name(col)

    if operator == "contains":
        return col.ilike(f"%{value}%")
    if operator == "startswith":
        return col.ilike(f"{value}%")
    if operator == "endswith":
        return col.ilike(f"%{value}")

    if operator == "gt":
        return col > _cast_scalar(value, col)
    if operator == "lt":
        return col < _cast_scalar(value, col)
    if operator == "gte":
        return col >= _cast_scalar(value, col)
    if operator == "lte":
        return col <= _cast_scalar(value, col)
    if operator == "in":
        return col.in_(_cast_list(value, col))

    if operator == "eq":
        # Optional fuzzy default for TEXT columns
        if DEFAULT_FUZZY_STRINGS and t in {"String", "VARCHAR", "Text"}:
            return col.ilike(f"%{value}%")
        return col == _cast_scalar(value, col)

    raise HTTPException(status_code=400, detail=f"Unsupported operator: {operator}")
