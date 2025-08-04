elastic_entities = {
    # ✅ Simple Entity
    "vendor": {
        "index_name": "vendor_index",
        "fields": ["id", "name", "email", "phone", "state_id"],
        "follow_fk": {
            "state": {
                "fields": ["id", "name", "code"]
            }
        },
        "flatten": True,
        "searchable_fields": ["name", "email", "state.name"],
        "weights": {"name": 2.0},
        "suggest_fields": ["name", "state.name"],
        "field_aliases": {"state.name": "stateName"},
        "analyzers": {"name": "edge_ngram_analyzer"},
    },

    # 🧠 Deep, Rich Entity (with multi-level FK)
    "item": {
        "index_name": "item_index",
        "__all__": True,
        "follow_fk": {
            "vendor": {
                "__all__": True,
                "follow_fk": {
                    "state": {
                        "fields": ["id", "name", "code"]
                    }
                }
            },
            "category": {
                "__all__": True,
                "follow_fk": {
                    "department": {
                        "fields": ["id", "name"]
                    }
                }
            },
            "secondary_category": {
                "fields": ["id", "name"]
            },
            "tax_group": {
                "__all__": True
            },
            "cash_discount_group": {
                "fields": ["id", "name", "discount_percent"]
            },
            "price_group": {
                "fields": ["id", "name", "markup_percent"]
            }
        },
        "flatten": True,
        "searchable_fields": [
            "name", "description", "item_code", "upc_code",
            "vendor.name", "vendor.state.name",
            "category.name", "category.department.name",
            "secondary_category.name", "tax_group.name"
        ],
        "field_aliases": {
            "vendor.name": "vendorName",
            "vendor.state.name": "vendorStateName",
            "category.name": "categoryName",
            "category.department.name": "departmentName",
            "secondary_category.name": "secondaryName",
            "tax_group.name": "taxGroupName"
        },
        "weights": {
            "name": 2.0,
            "description": 1.2,
            "item_code": 1.5,
            "vendor.name": 1.0
        },
        "suggest_fields": ["name", "item_code", "vendor.name"],
        "analyzers": {
            "name": "edge_ngram_analyzer",
            "item_code": "keyword_lowercase"
        },
        "exclude_if": lambda row: not row.get("active", True),
        "nested_fields": ["vendor", "tax_group"],
        "meta": {
            "refresh_interval": "1s",
            "number_of_shards": 1
        }
    },

    # 📦 Invoice indexing with FK to customer
    "invoice": {
        "index_name": "invoice_index",
        "fields": ["id", "date", "status"],
        "follow_fk": {
            "customer": {
                "fields": ["id", "name", "email"]
            },
            "salesperson": {
                "fields": ["id", "name"]
            },
            "store": {
                "fields": ["id", "name"]
            }
        },
        "flatten": True,
        "searchable_fields": ["id", "customer.name", "salesperson.name", "store.name"],
        "weights": {"customer.name": 1.5},
        "suggest_fields": ["id"],
        "field_aliases": {"customer.name": "customerName"}
    }
}
