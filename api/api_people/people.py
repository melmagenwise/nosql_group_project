import json
import os

from flask import Flask, jsonify, request
from pymongo import MongoClient
import redis


app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client["api_people"]
people_collection = db["people"]

r = redis.Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    db=int(os.environ.get("REDIS_DB", 0)),
)

CACHE_TTL_SECONDS = int(os.environ.get("CACHE_TTL_SECONDS", 60))


def serialize_document(document):
    serialized = {}
    for key, value in document.items():
        if key == "_id":
            serialized[key] = str(value)
        else:
            serialized[key] = value
    return serialized


def build_cache_key(prefix, *parts):
    normalized_parts = [part or "all" for part in parts]
    return ":".join([prefix, *normalized_parts])


@app.route("/people", methods=["GET"])
def get_people():
    search = request.args.get("q")
    limit_param = request.args.get("limit")

    try:
        limit = int(limit_param) if limit_param else None
    except ValueError:
        limit = None

    cache_key = build_cache_key("people", search or "", limit_param or "")
    cached = r.get(cache_key)
    if cached:
        print("people cache hit!")
        return jsonify(json.loads(cached))

    query = {}
    if search:
        query["name"] = {"$regex": search, "$options": "i"}

    cursor = people_collection.find(query)
    if limit:
        cursor = cursor.limit(max(limit, 1))

    documents = [serialize_document(item) for item in cursor]
    r.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(documents))
    return jsonify(documents)


@app.route("/people/<id>", methods=["GET"])
def get_person(id):
    cache_key = build_cache_key("people_detail", id)
    cached = r.get(cache_key)
    if cached:
        print("people detail cache hit!")
        return jsonify(json.loads(cached))

    query = {"$or": [{"_id": id}, {"imdb_name_id": id}]}
    document = people_collection.find_one(query)
    if not document:
        return jsonify({"error": "Person not found"}), 404

    serialized = serialize_document(document)
    r.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(serialized))
    return jsonify(serialized)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
