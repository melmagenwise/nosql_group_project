# Importing the 'pymongo' module for MongoDB interaction
import pymongo
import os 

# Definition of the PyMongoDatabase class
class DatabaseManagerClient:
    # Constructor method to initialize the database connection
    def __init__(self):
        try:
            # Creating a MongoClient to connect to the local MongoDB server
            mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
            self.client = pymongo.MongoClient(mongo_uri)
            # Getting the 'mongodb' database from the MongoDB server
            self.db = self.client['clients_db']
            # Getting the 'clients' collection from the 'mongodb' database
            self.collection = self.db['clients']
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

    # Exercice 1.2: Method to insert client data into the 'clients' collection
    def insert_client(self, client):
        try:
            # Creating a dictionary with client details
            data = {
                "_id": self.get_next_id(),
                'name': client.name,
                'birthday': client.birthday,
                'email': client.email,
                'phone': client.phone,
                'city': client.city,
                'genre': client.genre
            }
            # Inserting the client data into the 'clients' collection and obtaining the inserted name
            sid = self.collection.insert_one(data).inserted_id
            # Printing a message indicating the successful insertion of data with the obtained name
            print(f"client '{client.name}' inserted with ID: {sid}")
        except Exception as e:
            # Handling exceptions and printing an error message if data insertion fails
            print(f"Error: {e}")

    # Method to fetch a specific client's data based on client ID
    def fetch_client(self, sid):
        # Querying the 'clients' collection to find data for a specific client based on client ID
        data = self.collection.find_one({'_id': sid})
        return data

    # Method to fetch all clients' data from the 'clients' collection
    def fetch_clients(self):
        # Querying the 'clients' collection to find all data
        data = self.collection.find()
        return data
    
    # Method to fetch all clients' data from the 'clients' collection with filters and pagination
    def fetch_clients_filtered(self, filters=None, page=1, per=20):
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
    
    # Method to update a specific client's data based on client ID
    def update_client(self, sid, client):
        # Creating a dictionary with updated client details
        data = {
            'name': client.name,
            'birthday': client.birthday,
            'email': client.email,
            'phone': client.phone,
            'city': client.city,
            'genre': client.genre
        }
        # Updating the client data in the 'clients' collection
        self.collection.update_one({'_id': sid}, {"$set": data})

    # Method to delete a specific client's data based on client name
    def delete_client(self, name):
        # Deleting a client's data from the 'clients' collection based on client name
        self.collection.delete_one({'name': name})