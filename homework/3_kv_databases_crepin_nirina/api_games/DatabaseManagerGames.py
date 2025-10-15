# Importing the 'pymongo' module for MongoDB interaction
import pymongo
import os

# Definition of the PyMongoDatabase class
class DatabaseManagerGame:
    # Constructor method to initialize the database connection
    def __init__(self):
        try:
            # Creating a MongoClient to connect to the local MongoDB server
            mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
            self.client = pymongo.MongoClient(mongo_uri)
            # Getting the 'mongodb' database from the MongoDB server
            self.db = self.client['games_db']
            # Getting the 'games' collection from the 'mongodb' database
            self.collection = self.db['games']
        except Exception as e:
            # Handling exceptions and printing an error message if connection fails
            print(f"Error: {e}")

    # Method to close connection 
    def close(self):
        if self.client is not None:
            self.client.close()
            print("Connection closed.")

    # Excercice 2: Indexing - Get next available ID
    def get_next_id(self):
        last = self.collection.find_one(sort=[("_id", -1)])
        if last:
            return last["_id"] + 1
        else:
            return 1

    # Exercice 1.2: Method to insert game data into the 'games' collection
    def insert_game(self, game):
        try:
            # Creating a dictionary with game details
            data = {
                "_id": self.get_next_id(),
                'title': game.title,
                'year': game.year,
                'genre': game.genre,
                'platform': game.platform,
                'price': game.price,
                'quantity': game.quantity
            }
            # Inserting the game data into the 'games' collection and obtaining the inserted Title
            sid = self.collection.insert_one(data).inserted_id
            # Printing a message indicating the successful insertion of data with the obtained Title
            print(f"game '{game.title}' inserted with ID: {sid}")
        except Exception as e:
            # Handling exceptions and printing an error message if data insertion fails
            print(f"Error: {e}")

    # Method to fetch a specific game's data based on game ID
    def fetch_game(self, sid):
        # Querying the 'games' collection to find data for a specific game based on game ID
        data = self.collection.find_one({'_id': sid})
        return data

    # Method to fetch all games' data from the 'games' collection
    def fetch_games(self):
        # Querying the 'games' collection to find all data
        data = self.collection.find()
        return data
    
    # Method to fetch all games' data from the 'games' collection with filters and pagination
    def fetch_games_filtered(self, filters=None, page=1, per=20):
        query = filters or {}
        cursor = self.collection.find(query)
        # Simple pagination
        try:
            page = int(page) if page else 1
            per = int(per) if per else 0
        except Exception:
            page, per = 1, 0
        if per and per > 0:
            skip = max(0, (page - 1) * per)
            cursor = cursor.skip(skip).limit(per)
        return cursor

    # Method to update a specific game's data based on game ID
    def update_game(self, sid, game):
        # Creating a dictionary with updated game details
        data = {
            'title': game.title,
            'year': game.year,
            'genre': game.genre,
            'platform': game.platform,
            'price': game.price,
            'quantity': game.quantity
        }
        # Updating the game data in the 'games' collection
        self.collection.update_one({'_id': sid}, {"$set": data})

    # Method to delete a specific game's data based on game Title
    def delete_game(self, title):
        # Deleting a game's data from the 'games' collection based on game Title
        self.collection.delete_one({'title': title})