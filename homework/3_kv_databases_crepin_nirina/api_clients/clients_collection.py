from flask import Flask, request, jsonify
from DatabaseManagerClients import DatabaseManagerClient
from clients import Client
from cache import ping, delete, delete_prefix, get as cache_get, set as cache_set

import json
import hashlib

app = Flask(__name__)
db = DatabaseManagerClient()


# CRUD operations

# GET /clients/<id> - Get all video clients
@app.route("/clients", methods=["GET"])
def get_clients():
    
    page = request.args.get("page", "1")
    per = request.args.get("per", "20")
    genre = request.args.get("genre")
    city = request.args.get("city")
    q = request.args.get("q")

    if q is not None:
        base = json.dumps({k: request.args[k] for k in sorted(request.args)}, 
                          ensure_ascii=False, separators=(",", ":"))
        digest = hashlib.sha1(base.encode("utf-8")).hexdigest()
        cache_key = f"search:{digest}"
    else:
        parts = [f"page={page}", f"per={per}"]
        if genre:    
            parts.append(f"genre={genre}")
        if city: 
            parts.append(f"city={city}")
        cache_key = "clients:list:" + ":".join(parts)

    cached = cache_get(cache_key)
    if cached:
        return jsonify(json.loads(cached))
    
    filters = {}
    if genre:    
        filters["genre"] = genre
    if city: 
        filters["city"] = city

    clients = db.fetch_clients_filtered(filters=filters, page=page, per=per)
    result = []
    for g in clients:
        g["_id"] = str(g["_id"])  # ObjectId en string
        result.append(g)
    cache_set(cache_key, json.dumps(result))
    return jsonify(result)

# GET /clients/<id> - Get a specific video client
@app.route("/clients/<int:client_id>", methods=["GET"])
def get_client(client_id):
    cache_key = f"client:{client_id}"
    cached = cache_get(cache_key)
    if cached:
        return jsonify(json.loads(cached))
    client = db.fetch_client(client_id)
    if client:
        client["_id"] = str(client["_id"])
        cache_set(cache_key, json.dumps(client))
        return jsonify(client)
    return jsonify({"error": "client not found"}), 404

# POST /clients/<id> - Post a new video client
@app.route("/clients", methods=["POST"])
def add_client():
    data = request.json
    try:
        new_client = Client(
            sid=None,  
            name=data["name"],
            birthday=data["birthday"],
            email=data["email"],
            phone=data["phone"],
            city=data["city"],
            genre=data["genre"]
        )
        db.insert_client(new_client)

        # Exercice 8.3.d: cache invalidation
        delete_prefix("clients:list:")
        delete_prefix("clients:search:")

        return jsonify({"message": f"client '{new_client.name}' added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# PUT /clients/<id> - Update an existing video client
@app.route("/clients/<int:client_id>", methods=["PUT"])
def update_client(client_id):
    data = request.json
    try:
        updated_client = Client(
            sid=client_id,
            name=data.get("name", ""),
            birthday=data.get("birthday", ""),
            email=data.get("email", ""),
            phone=data.get("phone", ""),
            city=data.get("city", ""),
            genre=data.get("genre", "")
        )
        db.update_client(client_id, updated_client)
        
        # Exercice 8.3.d: cache invalidation
        delete(f"client:{client_id}")
        delete_prefix("clients:list:")
        delete_prefix("clients:search:")

        return jsonify({"message": "client updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# DELETE /clients/<id> - Remove a video client
@app.route("/clients/<int:client_id>", methods=["DELETE"])
def delete_client(client_id):
    client = db.fetch_client(client_id)
    if not client:
        return jsonify({"error": "client not found"}), 404
    db.collection.delete_one({"_id": client_id})

    # Exercice 8.3.d: cache invalidation
    delete(f"client:{client_id}")
    delete_prefix("clients:list:")
    delete_prefix("clients:search:")
    
    return jsonify({"message": "client deleted successfully"})

# Check endpoint for Redis
@app.route("/__ping/redis", methods=["GET"])
def redis_ping():
    return {"redis_ok": ping()}

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

