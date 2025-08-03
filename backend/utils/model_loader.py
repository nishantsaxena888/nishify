import importlib
import pkgutil

def get_model_class(client_name: str, entity_name: str):
    module_path = f"backend.clients.{client_name}.models.{entity_name}"
    mod = importlib.import_module(module_path)
    return getattr(mod, entity_name.capitalize())

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

