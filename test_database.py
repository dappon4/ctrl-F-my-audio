from pymongo.mongo_client import MongoClient


uri = "mongodb+srv://swastikagrawal3:NUw3CtIirJZHCqKR@ctrlf.9wvxvoo.mongodb.net/?retryWrites=true&w=majority"
cluster = MongoClient(uri)
db = cluster['predictions']
collection = db['data']
print(collection.find_one())
collection.insert_one({'category': 'hello', 'stamp': '0'})
print(list(collection.find()))