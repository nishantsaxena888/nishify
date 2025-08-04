import os
import json
import importlib.util

def get_client_name():
    return os.getenv("CLIENT_NAME", "pioneer_wholesale_inc")

def get_client_config():
    client = get_client_name()
    path = f"clients/{client}/config.json"
    if not os.path.exists(path):
        raise FileNotFoundError(f"No config file found for client {client}")
    return json.load(open(path))

def get_elastic_config():
    """
    Dynamically load elastic_entities.py for the active client.
    Returns: elastic_entities dict
    """
    client = get_client_name()
    path = f"clients/{client}/elastic_entities.py"
    if not os.path.exists(path):
        raise FileNotFoundError(f"elastic_entities.py not found for client '{client}'")

    spec = importlib.util.spec_from_file_location("elastic_entities", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.elastic_entities
