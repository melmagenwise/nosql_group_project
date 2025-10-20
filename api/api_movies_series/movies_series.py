import os
import json

from flask import Flask, jsonify, request
from pymongo import MongoClient
import redis


app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client["api_movies_series"]
movies_collection = db["movies_series"]


r = redis.Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    db=int(os.environ.get("REDIS_DB", 0)),
)

CACHE_TTL_SECONDS = int(os.environ.get("CACHE_TTL_SECONDS", 60))
CACHE_KEYS = {
    "all": "movies_series_all",
    "movies": "movies_only",
    "series": "series_only",
}

def build_payload(data, forced_type=None):
    if not data or not isinstance(data, dict) or "title" not in data:
        return None

    payload = dict(data)
    if forced_type:
        payload["imdb_type"] = forced_type
    else:
        payload.setdefault("imdb_type", "Movie")
    return payload


def serialize_document(doc):
    if not doc:
        return {}

    serialized = {}
    for key, value in doc.items():
        if key == "_id":
            serialized[key] = str(value)
        else:
            serialized[key] = value
    return serialized


def fetch_documents(filter_query=None):
    items = movies_collection.find(filter_query or {})
    return [serialize_document(item) for item in items]


@app.route("/movies-series", methods=["GET"])
def get_movies_series():
    cache_key = CACHE_KEYS["all"]
    cached = r.get(cache_key)
    if cached:
        print("cache hit!")
        return jsonify(json.loads(cached))

    print("cache miss Fetching from MongoDB...")
    items = fetch_documents()
    r.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(items))
    return jsonify(items)


@app.route("/movies", methods=["GET"])
def get_movies():
    cache_key = CACHE_KEYS["movies"]
    cached = r.get(cache_key)
    if cached:
        print("cache hit!")
        return jsonify(json.loads(cached))

    print("cache miss Fetching from MongoDB...")
    items = fetch_documents({"imdb_type": {"$regex": "^movie$", "$options": "i"}})
    r.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(items))
    return jsonify(items)


@app.route("/series", methods=["GET"])
def get_series():
    cache_key = CACHE_KEYS["series"]
    cached = r.get(cache_key)
    if cached:
        print("cache hit!")
        return jsonify(json.loads(cached))

    print("cache miss Fetching from MongoDB...")
    items = fetch_documents(
        {
            "$or": [
                {"imdb_type": {"$regex": "^tv", "$options": "i"}},
                {"imdb_type": {"$not": {"$regex": "^movie$", "$options": "i"}}},
            ]
        }
    )
    r.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(items))
    return jsonify(items)


@app.route("/movies-series", methods=["POST"])
def add_movies_series():
    payload = build_payload(request.get_json(silent=True))
    if not payload:
        return jsonify({"error": "please provide at least a title"}), 400

    result = movies_collection.insert_one(payload)
    document = movies_collection.find_one({"_id": result.inserted_id})
    r.delete(*CACHE_KEYS.values())
    return jsonify(serialize_document(document)), 201


@app.route("/movies", methods=["POST"])
def add_movies():
    payload = build_payload(request.get_json(silent=True), forced_type="Movie")
    if not payload:
        return jsonify({"error": "please provide at least a title"}), 400

    result = movies_collection.insert_one(payload)
    document = movies_collection.find_one({"_id": result.inserted_id})
    r.delete(*CACHE_KEYS.values())
    return jsonify(serialize_document(document)), 201


@app.route("/series", methods=["POST"])
def add_series():
    payload = build_payload(request.get_json(silent=True), forced_type="TVSeries")
    if not payload:
        return jsonify({"error": "please provide at least a title"}), 400

    result = movies_collection.insert_one(payload)
    document = movies_collection.find_one({"_id": result.inserted_id})
    r.delete(*CACHE_KEYS.values())
    return jsonify(serialize_document(document)), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
