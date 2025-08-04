from elasticsearch import Elasticsearch
from backend.utils.config import get_elastic_config

es = Elasticsearch("http://localhost:9200")
elastic_entities = get_elastic_config()


def search_elastic(entity: str, query: dict, page: int = 1, size: int = 20):
    if entity not in elastic_entities:
        raise ValueError(f"No elastic config for entity: {entity}")

    config = elastic_entities[entity]
    index_name = config["index_name"]
    searchable_fields = config.get("searchable_fields", [])

    must_clauses = []

    for field, value in query.items():
        # Only use if field is in the searchable list
        if field in searchable_fields:
            must_clauses.append({
                "match": {
                    field: {
                        "query": value,
                        "fuzziness": "AUTO"
                    }
                }
            })

    # If no valid filters were provided, return match_all
    if not must_clauses:
        body = {
            "query": {
                "match_all": {}
            },
            "from": (page - 1) * size,
            "size": size
        }
    else:
        body = {
            "query": {
                "bool": {
                    "must": must_clauses
                }
            },
            "from": (page - 1) * size,
            "size": size
        }

    print(f"[ElasticSearch] Querying index: {index_name} with filters: {query}")

    response = es.search(index=index_name, body=body)

    results = [hit["_source"] for hit in response["hits"]["hits"]]
    total = response["hits"]["total"]["value"]

    return {
        "items": results,
        "total": total,
        "page": page,
        "size": size
    }
