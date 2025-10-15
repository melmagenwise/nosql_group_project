from flask import Flask, request, jsonify
from DatabaseManagerGames import DatabaseManagerGame
from games import Game
from cache import ping, delete, delete_prefix, get as cache_get, set as cache_set

import json
import hashlib

app = Flask(__name__)
db = DatabaseManagerGame()


# CRUD operations

# GET /games/<id> - Get all video games
@app.route("/games", methods=["GET"])
def get_games():

    page = request.args.get("page", "1")
    per = request.args.get("per", "20")
    genre = request.args.get("genre")
    platform = request.args.get("platform")
    year = request.args.get("year")
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
        if platform: 
            parts.append(f"platform={platform}")
        if year:     
            parts.append(f"year={year}")
        cache_key = "games:list:" + ":".join(parts)

    cached = cache_get(cache_key)
    if cached:
        return jsonify(json.loads(cached))
    
    filters = {}
    if genre:    
        filters["genre"] = genre
    if platform: 
        filters["platform"] = platform
    if year:
        try:
            filters["year"] = int(year)
        except Exception:
            pass

    games = db.fetch_games_filtered(filters=filters, page=page, per=per)
    result = []
    for g in games:
        g["_id"] = str(g["_id"])  # ObjectId en string
        result.append(g)
    cache_set(cache_key, json.dumps(result))
    return jsonify(result)

# GET /games/<id> - Get a specific video game
@app.route("/games/<int:game_id>", methods=["GET"])
def get_game(game_id):
    cache_key = f"game:{game_id}"
    cached = cache_get(cache_key)
    if cached:
        return jsonify(json.loads(cached))
    game = db.fetch_game(game_id)
    if game:
        game["_id"] = str(game["_id"])
        cache_set(cache_key, json.dumps(game))
        return jsonify(game)
    return jsonify({"error": "Game not found"}), 404

# POST /games/<id> - Post a new video game
@app.route("/games", methods=["POST"])
def add_game():
    data = request.json
    try:
        new_game = Game(
            sid=None,  
            title=data["title"],
            year=int(data["year"]),
            genre=data["genre"],
            platform=data["platform"],
            price=float(data["price"]),
            quantity=int(data["quantity"])
        )
        db.insert_game(new_game)

        # Exercice 8.3.d: cache invalidation
        delete_prefix("games:list:")
        delete_prefix("games:search:")

        return jsonify({"message": f"Game '{new_game.title}' added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# PUT /games/<id> - Update an existing video game
@app.route("/games/<int:game_id>", methods=["PUT"])
def update_game(game_id):
    data = request.json
    try:
        updated_game = Game(
            sid=game_id,
            title=data.get("title", ""),
            year=int(data.get("year", 0)),
            genre=data.get("genre", ""),
            platform=data.get("platform", ""),
            price=float(data.get("price", 0)),
            quantity=int(data.get("quantity", 0))
        )
        db.update_game(game_id, updated_game)

        # Exercice 8.3.d: cache invalidation
        delete(f"game:{game_id}")
        delete_prefix("games:list:")
        delete_prefix("search:")

        return jsonify({"message": "Game updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# DELETE /games/<id> - Remove a video game
@app.route("/games/<int:game_id>", methods=["DELETE"])
def delete_game(game_id):
    game = db.fetch_game(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    db.collection.delete_one({"_id": game_id})
    
    # Exercice 8.3.d: cache invalidation
    delete(f"game:{game_id}")
    delete_prefix("games:list:")
    delete_prefix("search:")      

    return jsonify({"message": "Game deleted successfully"})

# Check endpoint for Redis
@app.route("/__ping/redis", methods=["GET"])
def redis_ping():
    return {"redis_ok": ping()}

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

