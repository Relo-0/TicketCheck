import json
from pathlib import Path

def load_sites_config(path="config/sites.json"):
    file_path = Path(path)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["sites"]
