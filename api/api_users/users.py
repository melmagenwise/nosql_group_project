import json
import os

from bson import ObjectId
from flask import Flask, jsonify, request
from pymongo import MongoClient
import redis


app = Flask(__name__)

# connexion to MongoDB
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017")) 
db = client["api_movies_series"]
my_friends_collection = db["my_friends"]
users_collection = db["users"]   # <-- ici on suppose que le profil et les favoris sont stockés ici

# connexion to Redis
r = redis.Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    db=int(os.environ.get("REDIS_DB", 0)),
)

CACHE_TTL_SECONDS = int(os.environ.get("CACHE_TTL_SECONDS", 60))


# Getting all of friends of the user
@app.route('/myfriends', methods=['GET'])
def get_my_friends():
    # Getting the data from the cache (Redis)
    cache_key = "my_friends_list" # name of the key in Redis
    cached_data =r.get(cache_key)
    if cached_data:
        print("cache hit!")
        return jsonify(json.loads(cached_data))
    # Getting the data from my_friends_collection (from MongoDB) if the data is not in the cache
    else:
        print("cache miss Fetching from MongoDB...")
        my_friends = list(my_friends_collection.find())
        for friend in my_friends:
            friend['_id'] = str(friend['_id'])
        #Storage of the value for 60''    
        r.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(my_friends)) 
        return jsonify(my_friends)
    
# Getting a friend with his id
@app.route('/my_friends/<friend_id>', methods=['GET'])
def get_my_friend(friend_id):
    # Getting the data from the cache (Redis)
    cache_key= f"friend:{friend_id}"
    cached_data = r.get(cache_key)
    if cached_data:
        print("cache hit!")
        return jsonify(json.loads(cached_data))
    # Getting the data from my_friends_collection (from MongoDB) if the data is not in the cache
    try:
        friend = my_friends_collection.find_one({"_id": ObjectId(friend_id)})
    except Exception:
        friend = my_friends_collection.find_one({"_id": friend_id})
    if friend:
        friend['_id'] = str(friend['_id'])
        r.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(friend))
        return jsonify(friend)
    return jsonify({'error': 'Friend not found'}), 404

# Getting my own profile myprofile
# URL example http://localhost:5000/myprofile?user_id=ur99999999
@app.route('/myprofile', methods=['GET'])
def get_profile():
    user_id = request.args.get('user_id', 'ur12345678')  # # example/myprofile?user_id=ur99999999 -> user_id = "ur99999999" sinon ur12345678 oar défaut
    cache_key = f"profile:{user_id}"
    cached_data = r.get(cache_key)
    if cached_data:
        print("cache hit! /myprofile")
        return jsonify(json.loads(cached_data))
    else:
        print("cache miss Fetching from MongoDB...")
        user = users_collection.find_one({"imdb_user_id": user_id})
        if user:
            user['_id'] = str(user['_id'])
            r.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(user))
            return jsonify(user)
        else:
            return jsonify({'error': 'Profile not found'}), 404


# Getting my own list of favorites
# URL example : http://localhost:5000/mylist?user_id=ur12345678&limit=5
@app.route('/mylist', methods=['GET'])
def get_my_list():
    user_id = request.args.get("user_id", "ur12345678")
    limit_param = request.args.get("limit", None)
    try:
        limit = int(limit_param) if limit_param else None
    except ValueError:
        limit = None
    cache_key = f"favorites:{user_id}:{limit if limit else 'all'}"
    cached_data = r.get(cache_key)
    if cached_data:
        print("cache hit! /mylist")
        return jsonify(json.loads(cached_data))
    else:
        print("cache miss Fetching from MongoDB...")
        doc = users_collection.find_one({"imdb_user_id": user_id}, {"_id": 0, "favorites": 1})
        if doc and "favorites" in doc:
            favorites = doc["favorites"]
            if limit:
                favorites = favorites[: limit if limit > 0 else 0]
            r.setex(cache_key, CACHE_TTL_SECONDS, json.dumps(favorites))
            return jsonify(favorites)
        else:
            return jsonify({"error": "Favorites not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)