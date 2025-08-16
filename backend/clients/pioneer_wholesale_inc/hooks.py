# Auto-generated hooks for pioneer_wholesale_inc
# Edit safely — re-runs will overwrite this file.
from __future__ import annotations
from typing import Any, Dict, List, Optional
import datetime

# ---- Per-entity defaults (generated) ----
ENTITY_DEFAULTS: Dict[str, Dict[str, Any]] = {
    "state": {    },
    "item_category": {    },
    "secondary_category": {    },
    "vendor": {    },
    "item": {        "active": true,    },
    "tax_group": {    },
    "cash_discount_group": {    },
    "price_group": {    },
    "inventory_location": {    },
    "inventory": {    },
    "salesperson": {    },
    "customer": {    },
    "purchase_order": {    },
    "purchase_order_item": {    },
    "invoice": {    },
    "invoice_item": {    },
}

def options(entity: str, schema: str = "basic") -> Dict[str, Any]:
    """
    Return options metadata for an entity.
    schema="basic" | "full"
    """
    # Place to compute selects / enums / cascades; keep minimal for now.
    return {
        "entity": entity,
        "schema": schema,
        "generated_for": "pioneer_wholesale_inc",
    }

def apply_defaults(entity: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Inject default values when missing.
    """
    defaults = ENTITY_DEFAULTS.get(entity) or {}
    out = dict(payload)
    for k, v in defaults.items():
        out.setdefault(k, v)
    # common timestamps if present in model
    if "created_at" in out and not out.get("created_at"):
        out["created_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    if "updated_at" in out:
        out["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    return out

def validate(entity: str, payload: Dict[str, Any]) -> List[str]:
    """
    Return a list of error strings, empty if valid.
    Extend per-entity rules if needed.
    """
    errors: List[str] = []
    # Example stub: required PKs handled by DB; add your own checks here.
    return errors

def before_insert(entity: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    return apply_defaults(entity, payload)

def after_insert(entity: str, record: Dict[str, Any]) -> Dict[str, Any]:
    return record

def before_update(entity: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    # Ensure updated_at moves if present
    out = dict(payload)
    if "updated_at" in out:
        out["updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
    return out

def after_update(entity: str, record: Dict[str, Any]) -> Dict[str, Any]:
    return record