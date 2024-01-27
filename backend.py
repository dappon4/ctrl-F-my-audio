from flask import Flask, request, send_file, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from mp4_to_mp3 import find_mp4
from mp3Clipper import split_mp3
from inference import inference
from flask_pymongo import PyMongo
import os

app = Flask(__name__)
CORS(app, origins='*')
api = Api(app)
app.config["SECRET KEY"] = '41bf9b4327c668b81f8f3f660eddb8f4bcfea2f8'
app.config["MONGO_URI"] = 'mongodb+srv://swastikagrawal3:Tu4mktXVe3HJKhLy@ctrlf.9wvxvoo.mongodb.net/?retryWrites=true&w=majority'

mongodb_client = PyMongo(app)
db = mongodb_client.db

type_map = {"angry_sound":0, "Bird":1, "Cats":2, "Dog":3, "guns":4}

class Convert(Resource):
    def post(self):
        file = request.files['uploaded_file']
        file.save('./assets/uploads/' + file.filename)
        mp3_name = find_mp4('./assets/uploads', './assets/mp3')
        split_mp3('./assets/chunks', 10)
        return jsonify({'data': mp3_name, 'message': 'File uploaded successfully'})

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
