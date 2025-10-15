import os
import json
from flask import Flask, jsonify, request, abort
import redis as redis_lib
import storage

app = Flask(__name__)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CACHE_TTL_SECONDS = 120
redis_client = redis_lib.Redis.from_url(REDIS_URL, decode_responses=True)


def _cache_get_json(key):
    raw = redis_client.get(key)
    if raw is None:
        return None
    return json.loads(raw)


def _cache_set_json(key, payload, ttl=CACHE_TTL_SECONDS):
    redis_client.setex(key, ttl, json.dumps(payload, separators=(",", ":")))


def _invalidate_after_write(game_id=None):
    if game_id is not None:
        redis_client.delete(f"game:{game_id}")
    keys = redis_client.keys("games:list*")
    for k in keys:
        redis_client.delete(k)


@app.errorhandler(400)
def bad_request(e):
    msg = getattr(e, "description", "Bad request")
    return jsonify({"error": msg}), 400


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


@app.get("/games")
def list_games():
    params = request.args.to_dict(flat=True)
    suffix_parts = []
    for key in sorted(params):
        value = params[key]
        if value not in (None, ""):
            suffix_parts.append(f"{key}={value}")
    suffix = "&".join(suffix_parts)

    if suffix:
        cache_key = f"games:list:{suffix}"
    else:
        cache_key = "games:list"

    cached = _cache_get_json(cache_key)
    if cached is not None:
        return jsonify(cached), 200

    items = storage.load_games()
    _cache_set_json(cache_key, items)
    return jsonify(items), 200


@app.get("/games/<int:game_id>")
def get_game(game_id: int):
    cache_key = f"game:{game_id}"
    cached = _cache_get_json(cache_key)

    if cached is not None:
        return jsonify(cached), 200

    items = storage.load_games()
    obj = storage.find_game(items, game_id)

    if obj is None:
        return jsonify({"error": "Not found"}), 404

    _cache_set_json(cache_key, obj)
    return jsonify(obj), 200


@app.post("/games")
def create_game():
    if not request.is_json:
        abort(400, description="Body must be application/json")

    payload = request.get_json()
    if not isinstance(payload, dict):
        abort(400, description="Body must be a JSON object")

    if "id" in payload:
        abort(400, description="Field 'id' is not allowed on creation")

    items = storage.load_games()
    new_id = storage.next_id(items)
    obj = {"id": new_id}

    for k, v in payload.items():
        if k != "id":
            obj[k] = v

    new_items = []
    if items is not None:
        new_items = list(items)
    new_items.append(obj)

    storage.save_games(new_items)
    _invalidate_after_write(game_id=new_id)

    return jsonify(obj), 201


@app.put("/games/<int:game_id>")
@app.patch("/games/<int:game_id>")
def update_game(game_id: int):
    if not request.is_json:
        abort(400, description="Body must be application/json")

    payload = request.get_json()
    if not isinstance(payload, dict):
        abort(400, description="Body must be a JSON object")

    if "id" in payload and payload["id"] != game_id:
        abort(400, description="Field 'id' cannot be modified")

    items = storage.load_games()
    if items is None:
        return jsonify({"error": "Not found"}), 404

    target = storage.find_game(items, game_id)
    if target is None:
        return jsonify({"error": "Not found"}), 404

    for k, v in payload.items():
        if k != "id":
            target[k] = v

    storage.save_games(items)
    _invalidate_after_write(game_id=game_id)

    return jsonify(target), 200


@app.delete("/games/<int:game_id>")
def delete_game(game_id: int):
    items = storage.load_games()
    if items is None:
        return jsonify({"error": "Not found"}), 404

    ok = storage.delete_game(items, game_id)
    if not ok:
        return jsonify({"error": "Not found"}), 404

    storage.save_games(items)
    _invalidate_after_write(game_id=game_id)

    return "", 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
