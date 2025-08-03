import os
import sys

def get_client_paths():
    if len(sys.argv) < 2:
        raise ValueError("Client name must be passed as an argument. Usage: python script.py <client_name>")
    
    client_name = sys.argv[-1]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.abspath(os.path.join(script_dir, ".."))
    client_dir = os.path.join(root_dir, "clients", client_name)
    entities_path = os.path.join(client_dir, "entities.py")
    output_path = os.path.join(client_dir, "entities.data.py")
    
    return script_dir, root_dir, client_dir, entities_path, output_path
