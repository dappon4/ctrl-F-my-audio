from pymongo.mongo_client import MongoClient


uri = "mongodb+srv://dahong:2RE7PgrEGqEDTpdE@ctrlf.9wvxvoo.mongodb.net/?retryWrites=true&w=majority"
cluster = MongoClient(uri)
db = cluster['prediction']
collection = db['data']
print(collection.find_one())
collection.insert_one({'category': 'hello', 'stamp': '0'})
print(list(collection.find()))