from flask import Flask, jsonify
from pymongo import MongoClient
import os
import redis
from bson import ObjectId
import json

app = Flask(__name__)

# connexion to MongoDB
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017")) 
db = client["api_movies_series"]
my_friends_collection = db["my_friends"]

# connexion to Redis
r = redis.Redis(
    host=os.environ.get("REDIS_HOST"), 
    port=6379,
    db=0  
)

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
        r.setex(cache_key, 60, json.dumps(my_friends)) #storage of the value for 60''
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
    friend = my_friends_collection.find_one({"_id": ObjectId(friend_id)}) # _id is an ObjectID type in MongoDB
    if friend:
        friend['_id'] = str(friend['_id'])
        r.setex(cache_key, 60, json.dumps(friend))
        return jsonify(friend)
    return jsonify({'error': 'Friend not found'}), 404