from flask import Flask, request, send_file, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from mp4_to_mp3 import find_mp4
from mp3Clipper import split_mp3
from inference import inference
from pymongo.mongo_client import MongoClient
import os

app = Flask(__name__)
CORS(app, origins='*')
api = Api(app)
app.config["SECRET KEY"] = '41bf9b4327c668b81f8f3f660eddb8f4bcfea2f8'

# uri = "mongodb://localhost:27017"
# client = MongoClient('localhost', 27017)
uri = "mongodb+srv://swastikagrawal3:NUw3CtIirJZHCqKR@ctrlf.9wvxvoo.mongodb.net/?retryWrites=true&w=majority&connectTimeoutMS=300000"
cluster = MongoClient(uri)
db = cluster['predictions']
# db = client['predictions']

def create_dict():  
    with open("index.txt", "r") as file:
            text = file.read()
            tags = text.split("\n")
    res = {}
    for i,name in enumerate(tags):
        res[name] = i
    
    return res
        

type_map = create_dict()

class Convert(Resource):
    def post(self):
        step = 3
        file = request.files['uploaded_file']
        file.save(os.path.join("assets","uploads",file.filename))
        mp3_name = find_mp4(os.path.join("assets", "uploads"), os.path.join("assets", "mp3"))
        split_mp3(os.path.join("assets","chunks"), step)
        tags = inference(os.path.join('models','acc-77.pth'), os.path.join("assets","chunks"), type_map,step)
        print(tags)
        db.drop_collection('data')
        collection = db.create_collection('data')
        for tag in tags:
            for k,v in dict(tag).items():
                collection.insert_one({'category': v, 'stamp': k})

        return jsonify({'data': tags, 'message': 'File uploaded successfully'})

class Clear(Resource):
    def post(self):
        try:
            uploads = [f for f in os.listdir('./assets/uploads')]
            mp3s = [f for f in os.listdir('./assets/mp3')]
            chunks = [f for f in os.listdir('./assets/chunks')]

            for i in uploads:
                os.remove(os.path.join('./assets/uploads',i))
            for i in mp3s:
                os.remove(os.path.join('./assets/mp3',i))
            for i in chunks:
                os.remove(os.path.join('./assets/chunks',i))
            
            return jsonify({'message': 'Cleared successfully'})

        except: 
            return jsonify({'message': 'Not Cleared'})
    
    def get(self):
        return jsonify({'number': len(os.listdir('./assets/uploads'))})


class Getall(Resource):
    def get(self):
        dic = {}
        data = db.data.find({})
        for entry in data:
            data[int(entry["stamp"])] = entry["category"]
        
        data.sort()
        return jsonify({'data': dic})

class Query(Resource):
    def post(self,k):
        data = request.get_json()
        query = k

        db.data.insert_one(data)
        return jsonify({'message': 'Data saved successfully'})

    
    
    def get(self,k):
        
        dic = {k:[]}
        
        data = db.data.find({'category': k})
        for entry in data:
            dic[k].append(int(entry["stamp"]))
        
        return jsonify({'data': dic})

api.add_resource(Convert, '/convert')
api.add_resource(Clear, '/clear')
api.add_resource(Query, '/query/<string:k>')
api.add_resource(Getall, '/getall')


if __name__ == '__main__':
    app.run(debug=True)
