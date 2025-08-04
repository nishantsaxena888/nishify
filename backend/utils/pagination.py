from sqlalchemy import Select

def apply_pagination(query: Select, page: int = 1, size: int = 20):
    offset = (page - 1) * size
    return query.limit(size).offset(offset)

def paginated_response(items, page: int, size: int, total: int):
    return {
        "items": items,
        "page": page,
        "size": size,
        "total": total
    }
