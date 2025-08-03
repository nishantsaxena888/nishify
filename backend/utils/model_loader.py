import importlib

def get_model_class(client_name: str, entity_name: str):
    module_path = f"backend.clients.{client_name}.models.{entity_name}"
    mod = importlib.import_module(module_path)
    return getattr(mod, entity_name.capitalize())
