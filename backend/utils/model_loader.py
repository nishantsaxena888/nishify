import importlib
import pkgutil

from importlib import import_module
import re

def _camelize(name: str) -> str:
    # "cash_discount_group" -> "CashDiscountGroup"
    parts = re.split(r'[_\W]+', name.strip())
    return "".join(p.capitalize() for p in parts if p)

def get_model_class(client_name: str, entity_name: str):
    module_path = f"backend.clients.{client_name}.models.{entity_name}"
    mod = import_module(module_path)
    
    # ✅ First try the proper camelized name
    cls_name = _camelize(entity_name)
    if hasattr(mod, cls_name):
        return getattr(mod, cls_name)

    # ✅ Optional: Try also exact entity_name in case it's already correct
    if hasattr(mod, entity_name):
        return getattr(mod, entity_name)

    # ❌ No wrong capitalize fallback — instead, clear error
    raise AttributeError(
        f"Model class not found for entity '{entity_name}'. "
        f"Tried: {cls_name} in module {module_path}"
    )

def get_all_models(client_name: str):
    models = []
    module_path = f"backend.clients.{client_name}.models"

    try:
        package = importlib.import_module(module_path)
    except ModuleNotFoundError:
        raise RuntimeError(f"Could not find models package for client '{client_name}'")

    for _, mod_name, _ in pkgutil.iter_modules(package.__path__):
        mod = importlib.import_module(f"{module_path}.{mod_name}")
        for attr in dir(mod):
            obj = getattr(mod, attr)
            if hasattr(obj, "__table__"):
                models.append(obj)

    return models

