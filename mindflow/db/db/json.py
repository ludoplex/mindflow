import json
import os

from typing import List
from typing import Optional

from mindflow.db.db.database import Database


def get_mindflow_dir():
    if os.name == "nt":  # Check if the OS is Windows
        config_dir = os.getenv("APPDATA")
    else:
        config_dir = os.path.join(os.path.expanduser("~"), ".config")
    return os.path.join(config_dir, "mindflow")


MINDFLOW_DIR = get_mindflow_dir()
if not os.path.exists(MINDFLOW_DIR):
    os.makedirs(MINDFLOW_DIR)


def create_and_load_json(path: str) -> dict:
    if os.path.exists(path):
        with open(path, "r+", encoding="utf-8") as json_file:
            return json.load(json_file)
    with open(path, "w", encoding="utf-8") as json_file:
        json.dump({}, json_file)
    return {}


JSON_DATABASE_PATH = os.path.join(MINDFLOW_DIR, "db.json")


class JsonDatabase(Database):
    def __init__(self):
        self.collections: dict = create_and_load_json(JSON_DATABASE_PATH)

    def load(self, collection: str, object_id: str) -> Optional[dict]:
        objects = self.collections.get(collection, None)
        return None if not objects else objects.get(object_id, None)

    def load_bulk(self, collection: str, object_ids: List[str]) -> List[Optional[dict]]:
        if objects := self.collections.get(collection, None):
            return [objects.get(object_id, None) for object_id in object_ids]
        else:
            return []

    def delete(self, collection: str, object_id: str):
        if objects := self.collections.get(collection, None):
            objects.pop(object_id, None)
        else:
            return None

    def delete_bulk(self, collection: str, object_ids: List[str]):
        objects = self.collections.get(collection, None)
        if not objects:
            return None

        for object_id in object_ids:
            objects.pop(object_id, None)

    def save(self, collection: str, value: dict):
        objects = self.collections.get(collection, {})
        if objects == {}:
            self.collections[collection] = objects

        if object_id := value.get("id", None):
            objects[object_id] = value
        else:
            raise ValueError("No ID found in object")

    def save_bulk(self, collection: str, values: List[dict]):
        objects = self.collections.get(collection, {})
        if objects == {}:
            self.collections[collection] = objects

        for value in values:
            if object_id := value.get("id", None):
                objects[object_id] = value
            else:
                raise ValueError("No ID found in object")

    def save_file(self):
        with open(JSON_DATABASE_PATH, "w", encoding="utf-8") as json_file:
            json.dump(self.collections, json_file, indent=4)


JSON_DATABASE = JsonDatabase()
