entities = {

    "state": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "name": {"type": "str", "required": True}
        },
        "sample_data": [
            {"id": 1, "name": "California"},
            {"id": 2, "name": "Texas"},
            {"id": 3, "name": "New York"}
        ]
    },
    "item_category": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "name": {"type": "str", "required": True},
            "description": {"type": "str"},
        },
        "sample_data": [
            {"id": 1, "name": "Beverages", "description": "Cold drinks and juices"}
        ]
    },
    "secondary_category": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "name": {"type": "str", "required": True},
            "description": {"type": "str"},
        },
        "sample_data": [
            {"id": 1, "name": "Energy Drinks", "description": "Boost, Red Bull"}
        ]
    },
    "vendor": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "name": {"type": "str", "required": True},
            "address": {"type": "str"},
            "email": {"type": "str"},
            "phone": {"type": "str"},
            "contact_person": {"type": "str"},
            "state_id": {
                "type": "int",
                "foreign_key": "state.id"
            }
        },
        "sample_data": [
            {"id": 1, "name": "Coca-Cola Co.", "phone": "1234567890"}
        ]
    },
    "item": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "item_code": {"type": "str", "required": True},
            "name": {"type": "str", "required": True},
            "category_id": {
                "type": "int",
                "foreign_key": "item_category.id",
                "relation_type": "many-to-one"
            },
            "secondary_category_id": {
                "type": "int",
                "foreign_key": "secondary_category.id",
                "relation_type": "many-to-one"
            },
            "vendor_id": {
                "type": "int",
                "foreign_key": "vendor.id",
                "relation_type": "many-to-one"
            },
            "tax_group_id": {
                "type": "int",
                "foreign_key": "tax_group.id",
                "relation_type": "many-to-one"
            },
            "price_group_id": {
                "type": "int",
                "foreign_key": "price_group.id",
                "relation_type": "many-to-one"
            },
            "cash_discount_group_id": {
                "type": "int",
                "foreign_key": "cash_discount_group.id",
                "relation_type": "many-to-one"
            },
            "upc_code": {"type": "str"},
            "unit": {"type": "str"},
            "price": {"type": "float"},
            "description": {"type": "str"},
            "active": {"type": "bool", "default": True}
        },
        "sample_data": [
            {"id": 1, "item_code": "COKE500", "name": "Coke 500ml", "price": 1.25}
        ]
    },
    "tax_group": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "name": {"type": "str"},
            "tax_percent": {"type": "float"},
        },
        "sample_data": [
            {"id": 1, "name": "Standard Tax", "tax_percent": 7.5}
        ]
    },
    "cash_discount_group": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "name": {"type": "str"},
            "discount_percent": {"type": "float"},
            "terms": {"type": "str"},
        },
        "sample_data": [
            {"id": 1, "name": "5% Net 15", "discount_percent": 5.0, "terms": "Net 15 days"}
        ]
    },
    "price_group": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "name": {"type": "str"},
            "markup_percent": {"type": "float"},
        },
        "sample_data": [
            {"id": 1, "name": "Retail Pricing", "markup_percent": 12.5}
        ]
    },
    "inventory_location": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "name": {"type": "str"},
            "address": {"type": "str"},
        },
        "sample_data": [
            {"id": 1, "name": "Warehouse A"}
        ]
    },
    "inventory": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "item_id": {
                "type": "int",
                "foreign_key": "item.id",
                "relation_type": "many-to-one"
            },
            "location_id": {
                "type": "int",
                "foreign_key": "inventory_location.id",
                "relation_type": "many-to-one"
            },
            "quantity": {"type": "int"},
        },
        "sample_data": [
            {"id": 1, "item_id": 1, "location_id": 1, "quantity": 150}
        ]
    },
    "salesperson": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "name": {"type": "str"},
            "email": {"type": "str"},
            "phone": {"type": "str"},
        },
        "sample_data": [
            {"id": 1, "name": "Ravi", "email": "ravi@jnq.com"}
        ]
    },
    "customer": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "name": {"type": "str"},
            "address": {"type": "str"},
            "email": {"type": "str"},
            "phone": {"type": "str"},
            "salesperson_id": {
                "type": "int",
                "foreign_key": "salesperson.id",
                "relation_type": "many-to-one"
            },
            "credit_limit": {"type": "float"},
        },
        "sample_data": [
            {"id": 1, "name": "Big Retailer Inc", "phone": "9999999999"}
        ]
    },
    "purchase_order": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "vendor_id": {
                "type": "int",
                "foreign_key": "vendor.id",
                "relation_type": "many-to-one"
            },
            "date": {"type": "datetime"},
            "status": {"type": "str"},
        },
        "sample_data": [
            {"id": 1, "vendor_id": 1, "date": "2024-07-01T10:00:00", "status": "Submitted"}
        ]
    },
    "purchase_order_item": {
    "fields": {
        "id": {"type": "int", "primary_key": True},
        "po_id": {
            "type": "int",
            "foreign_key": "purchase_order.id",
            "relation_type": "many-to-one"
        },
        "item_id": {
            "type": "int",
            "foreign_key": "item.id",
            "relation_type": "many-to-one"
        },
        "quantity": {"type": "int"},
        "unit_price": {"type": "float"},
        },
        "unique_together": [["po_id", "item_id"]],
        "sample_data": [
            {"po_id": 1, "item_id": 1, "quantity": 100, "unit_price": 1.05}
        ]
    },
    "invoice": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
            "customer_id": {
                "type": "int",
                "foreign_key": "customer.id",
                "relation_type": "many-to-one"
            },
            "date": {"type": "datetime"},
            "status": {"type": "str"},
        },
        "sample_data": [
            {"id": 1, "customer_id": 1, "date": "2024-08-01T09:00:00", "status": "Draft"}
        ]
    },
    "invoice_item": {
        "fields": {
            "id": {"type": "int", "primary_key": True},
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
            "price": {"type": "float"},
        },
        # enforce uniqueness on the business key
        "unique_together": [["invoice_id", "item_id"]],
        "sample_data": [
            {"id": 1, "invoice_id": 1, "item_id": 1, "quantity": 5, "price": 1.25}
        ]
    }
}
