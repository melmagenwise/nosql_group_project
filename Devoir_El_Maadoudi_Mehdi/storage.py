import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "vgstore")

_client = MongoClient(MONGO_URI)
_db = _client[MONGO_DB]
_col = _db["games"]


def load_games():
    items = []
    cursor = _col.find({}, {"_id": 0})

    for doc in cursor:
        clean = {}
        for key, value in doc.items():
            clean[key] = value
        items.append(clean)

    return items


def save_games(items):
    _col.delete_many({})

    if not items:
        return

    for obj in items:
        # faire une copie profonde 'simple'
        doc = {}
        for k, v in obj.items():
            doc[k] = v
        _col.insert_one(doc)


def next_id(items):
    max_id = 0

    if items is None:
        return 1

    for obj in items:
        value = obj.get("id", 0)
        try:
            int_value = int(value)
        except (ValueError, TypeError):
            int_value = 0

        if int_value > max_id:
            max_id = int_value

    return max_id + 1


def find_game(items, game_id):
    try:
        gid = int(game_id)
    except (ValueError, TypeError):
        return None

    if items is None:
        return None

    for obj in items:
        if obj.get("id") == gid:
            return obj

    return None


def delete_game(items, game_id):
    try:
        gid = int(game_id)
    except (ValueError, TypeError):
        return False

    if items is None:
        return False

    index_to_delete = -1

    current_index = 0
    for obj in items:
        value = obj.get("id")
        if value == gid:
            index_to_delete = current_index
            break
        current_index += 1

    if index_to_delete == -1:
        return False

    del items[index_to_delete]
    return True
