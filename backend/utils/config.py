import os
import json

def get_client_name():
    return os.getenv("CLIENT_NAME", "pioneer_wholesale_inc")

def get_client_config():
    client = get_client_name()
    path = f"clients/{client}/config.json"
    if not os.path.exists(path):
        raise FileNotFoundError(f"No config file found for client {client}")
    return json.load(open(path))
