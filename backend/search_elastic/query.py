# backend/search_elastic/query.py
from elasticsearch import Elasticsearch
from backend.utils.config import get_elastic_config
from fastapi import HTTPException
from typing import Optional, Set

es = Elasticsearch("http://localhost:9200")
elastic_entities = get_elastic_config()


# -------------------- helpers --------------------
def _to_bool(v: str) -> bool:
    s = str(v).strip().lower()
    if s in {"true", "1", "yes", "y"}:
        return True
    if s in {"false", "0", "no", "n"}:
        return False
    raise HTTPException(status_code=400, detail=f"Invalid boolean: {v}")


def _cast_scalar(v: str):
    s = v.strip()
    if s.isdigit():
        return int(s)
    try:
        return float(s)
    except ValueError:
        pass
    if s.lower() in {"true", "false", "1", "0", "yes", "no"}:
        return _to_bool(s)
    return s


def _keyword(field: str) -> str:
    # Use keyword subfield for exact/terms/wildcard/prefix/sort on text fields
    return f"{field}.keyword"


def _sort_key_for(field: str, numeric_fields: Set[str]) -> str:
    # If field is numeric (per config), sort on the field itself; else use .keyword
    return field if field in numeric_fields else _keyword(field)


# -------------------- main --------------------
def search_elastic(
    entity: str,
    query: dict,
    page: int = 1,
    size: int = 20,
    sort: Optional[str] = None,
):
    if entity not in elastic_entities:
        raise ValueError(f"No elastic config for entity: {entity}")

    config = elastic_entities[entity]
    index_name = config["index_name"]

    # Optional config controls
    searchable_fields: Set[str] = set(config.get("searchable_fields", []))
    numeric_fields: Set[str] = set(config.get("numeric_fields", []))  # e.g. {"price", "quantity"}

    # Gate only text operators by searchable_fields
    text_ops = {"contains", "startswith", "endswith"}  # add "eq" here if you want to gate exact text too

    must_clauses = []

    for field, value in query.items():
        if value is None or value == "":
            continue

        # Parse operator
        if "__" in field:
            fname, op = field.split("__", 1)
        else:
            fname, op = field, "eq"

        # Respect searchable_fields ONLY for text operators
        if searchable_fields and op in text_ops and fname not in searchable_fields:
            # Text search not allowed on this field via config
            continue

        val = _cast_scalar(value)
        kw = _keyword(fname)

        # --- operator translations ---
        if op == "contains":
            # Note: wildcard on keyword is case-sensitive
            must_clauses.append({"wildcard": {kw: f"*{value}*"}})
        elif op == "startswith":
            must_clauses.append({"prefix": {kw: str(value)}})
        elif op == "endswith":
            must_clauses.append({"wildcard": {kw: f"*{value}"}})
        elif op == "in":
            vals = [_cast_scalar(x) for x in str(value).split(",") if x.strip()]
            must_clauses.append({"terms": {kw: vals}})
        elif op in {"gt", "gte", "lt", "lte"}:
            must_clauses.append({"range": {fname: {op: val}}})
        elif op == "eq":
            # term works for strings/bools/ints; if numeric, mapping should be numeric
            must_clauses.append({"term": {kw: val}})
        else:
            # Fallback: fuzzy match on analyzed field
            must_clauses.append({
                "match": {
                    fname: {
                        "query": value,
                        "fuzziness": "AUTO"
                    }
                }
            })

    # Build ES body
    if not must_clauses:
        body = {
            "query": {"match_all": {}},
            "from": max(0, (page - 1) * size),
            "size": max(1, size),
        }
    else:
        body = {
            "query": {"bool": {"must": must_clauses}},
            "from": max(0, (page - 1) * size),
            "size": max(1, size),
        }

    # Sorting
    if sort:
        if sort.startswith("-"):
            field = sort[1:]
            order = "desc"
        else:
            field = sort
            order = "asc"
        body["sort"] = [{_sort_key_for(field, numeric_fields): {"order": order}}]

    print(f"[ElasticSearch] Querying index: {index_name} with filters: {query}")
    print("[ElasticSearch] Body:", body)

    # ES 8/9 client still accepts 'body=' form
    resp = es.search(index=index_name, body=body)

    hits = resp.get("hits", {}).get("hits", [])
    items = [h.get("_source", {}) for h in hits]
    total = resp.get("hits", {}).get("total", {}).get("value", 0)

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
    }
