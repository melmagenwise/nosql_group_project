"""
A simple JSON API using Flask for a video game store with MongoDB and Redis.
"""
from flask import Flask, jsonify, request
from pymongo import MongoClient #to enable connection to MongoDB
from bson import ObjectId 
import os
import redis 
import json  

app = Flask(__name__)
#connexion to MongoDB
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017")) #connectiob to MongoDB
db = client["video_game_store_api"]
games_collection = db["games"]
clients_collection = db["clients"]

#connection to Redis
r = redis.Redis(
    host=os.environ.get("REDIS"), 
    port=6379,
    db=0  
)

@app.route('/games', methods=['GET'])
def get_games():
    cache_key = "game_list" #name of the key
    cached_data =r.get(cache_key)
    if cached_data:
        print("cache hit!")
        return jsonify(json.loads(cached_data))
    else:
        print("cache miss Fetching from MongoDB...")
        games = list(games_collection.find())
        for game in games:
            game['_id'] = str(game['_id'])
        r.setex(cache_key, 60, json.dumps(games))
        return jsonify(games)

@app.route('/games/<game_id>', methods=['GET'])
def get_game(game_id):

    cache_key= "game:{game_id}"
    cached_data = r.get(cache_key)
    if cached_data:
        print("cache hit!")
        return jsonify(json.loads(cached_data))

    game = games_collection.find_one({"_id": game_id})
    if game:
        game['_id'] = str(game['_id'])
        return jsonify(game)
    return jsonify({'error': 'Game not found'}), 404

@app.route('/games', methods=['POST'])
def add_game():
    data = request.get_json()
    if not data or 'title' not in data or 'platform' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    new_game = {"title": data['title'], "platform": data['platform']}
    result = games_collection.insert_one(new_game)
    new_game['_id'] = str(result.inserted_id)
    return jsonify(new_game), 201

@app.route('/games/<game_id>', methods=['PUT'])
def update_game(game_id):
    data = request.get_json()
    if not data or 'title' not in data or 'platform' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    result = games_collection.update_one(
        {"_id": game_id},
        {"$set": {"title": data['title'], "platform": data['platform']}}
    )
    if result.matched_count:
        game = games_collection.find_one({"_id": game_id})
        game['_id'] = str(game['_id'])
        r.delete("game:{game_id}")
        r.delete("games_list")
        return jsonify(game)
    return jsonify({'error': 'Game not found'}), 404

@app.route('/games/<game_id>', methods=['DELETE'])
def delete_game(game_id):
    result = games_collection.delete_one({"_id": game_id})
    if result.deleted_count:
        r.delete("game:{game_id}")
        r.delete("games_list")
        return jsonify({'message': 'Game deleted'})
    return jsonify({'error': 'Game not found'}), 404

@app.route('/clients', methods=['POST'])
def add_client():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Invalid data'}), 400
    new_client = {"name": data['name'], "email": data['email']}
    result = clients_collection.insert_one(new_client)
    new_client['_id'] = str(result.inserted_id)
    return jsonify(new_client), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)