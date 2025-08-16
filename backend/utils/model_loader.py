import importlib
import pkgutil
from importlib import import_module
import re
import inspect

def _camelize(name: str) -> str:
    # "cash_discount_group" -> "CashDiscountGroup"
    parts = re.split(r'[_\W]+', name.strip())
    return "".join(p.capitalize() for p in parts if p)

def _to_snake(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()

def get_model_class(client_name: str, entity_name: str):
    module_path = f"backend.clients.{client_name}.models.{entity_name}"
    mod = import_module(module_path)

    # preferred class name from entity
    cls_name = _camelize(entity_name)
    if hasattr(mod, cls_name):
        return getattr(mod, cls_name)

    # fallback: direct attribute
    if hasattr(mod, entity_name):
        return getattr(mod, entity_name)

    # last resort: any declarative class with matching __tablename__
    for obj in mod.__dict__.values():
        if inspect.isclass(obj) and getattr(obj, "__tablename__", None) == entity_name:
            return obj

    raise AttributeError(
        f"Model class not found for entity '{entity_name}'. "
        f"Tried: {cls_name} in module {module_path}"
    )

def get_all_models(client_name: str):
    models = []
    module_path = f"backend.clients.{client_name}.models"
    try:
        package = importlib.import_module(module_path)
    except ModuleNotFoundError as e:
        raise RuntimeError(f"Could not find models package for client '{client_name}'") from e

    for _, mod_name, ispkg in pkgutil.iter_modules(package.__path__):
        if ispkg or mod_name.startswith("_"):
            continue
        m = importlib.import_module(f"{module_path}.{mod_name}")
        for obj in m.__dict__.values():
            if inspect.isclass(obj) and getattr(obj, "__table__", None) is not None:
                models.append(obj)
    return models
