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

uri = "mongodb+srv://swastikagrawal3:NUw3CtIirJZHCqKR@ctrlf.9wvxvoo.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
db = client.predictions
print(db.data.find())

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
        tags = inference(os.path.join('models','acc-69.pth'), os.path.join("assets","chunks"), type_map,step)
        
        for tag in tags:
            db.data.insert_one(tag)
        
        return jsonify({'data': mp3_name, 'message': 'File uploaded successfully','base':{
            db.data.find()
        }})

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


class Query(Resource):
    def post(self,k):
        data = request.get_json()
        query = k

        db.data.insert_one(data)
        return jsonify({'message': 'Data saved successfully'})

api.add_resource(Convert, '/convert')
api.add_resource(Clear, '/clear')
api.add_resource(Query, '/query/<string:k>')


if __name__ == '__main__':
    app.run(debug=True)
