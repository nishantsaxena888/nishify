
entities = {
    "product": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "name": {"type": "str", "required": True},
            "price": {"type": "float"},
            "in_stock": {"type": "bool"}
        },
        "sample_data": [
            {"id": 1, "name": "Sample Product", "price": 9.99, "in_stock": True}
        ]
    }
}
entities = {
    "customer": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "name": {"type": "str", "required": True},
            "email": {"type": "str"},
        },
        "sample_data": [
            {"id": 1, "name": "Alice Corp", "email": "alice@example.com"},
            {"id": 2, "name": "Beta LLC", "email": "beta@example.com"}
        ]
    },
    "vendor": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "name": {"type": "str", "required": True},
        },
        "sample_data": [
            {"id": 1, "name": "Vendor A"},
            {"id": 2, "name": "Vendor B"}
        ]
    },
    "item": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "name": {"type": "str"},
            "price": {"type": "float"},
            "vendor_id": {
                "type": "int",
                "foreign_key": "vendor.id",
                "relation_type": "many-to-one",
                "related_name": "items"
            }
        },
        "sample_data": [
            {"id": 1, "name": "Widget", "price": 10.5, "vendor_id": 1},
            {"id": 2, "name": "Gadget", "price": 5.75, "vendor_id": 2}
        ]
    },
    "inventory": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "item_id": {
                "type": "int",
                "foreign_key": "item.id",
                "relation_type": "many-to-one",
                "related_name": "inventory_entries"
            },
            "quantity": {"type": "int"}
        },
        "sample_data": [
            {"id": 1, "item_id": 1, "quantity": 100},
            {"id": 2, "item_id": 2, "quantity": 50}
        ]
    },
    "invoice": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "customer_id": {
                "type": "int",
                "foreign_key": "customer.id",
                "relation_type": "many-to-one",
                "related_name": "invoices"
            },
            "date": {"type": "datetime"},
        },
        "sample_data": [
            {"id": 1, "customer_id": 1, "date": "2024-08-01T10:00:00"},
            {"id": 2, "customer_id": 2, "date": "2024-08-02T11:00:00"}
        ]
    },
    "invoice_item": {
        "fields": {
            "invoice_id": {
                "type": "int",
                "foreign_key": "invoice.id",
                "relation_type": "many-to-one"
            },
            "item_id": {
                "type": "int",
                "foreign_key": "item.id",
                "relation_type": "many-to-one"
            },
            "quantity": {"type": "int"},
        },
        "sample_data": [
            {"invoice_id": 1, "item_id": 1, "quantity": 2},
            {"invoice_id": 1, "item_id": 2, "quantity": 3}
        ]
    }
}
