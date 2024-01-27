from flask import Flask, request, send_file, jsonify, make_response
from flask_restful import Api, Resource
from flask_cors import CORS
from mp4_to_mp3 import *
from mp3Clipper import *
import os

app = Flask(__name__)
CORS(app,origins= '*')
api = Api(app)

type_map = {"angry_sound":0, "Bird":1, "Cats":2, "Dog":3, "guns":4}

class Convert(Resource):
    def post(self):
        file = request.files['uploaded_file']
        print(file)
        file.save('./assets/uploads/' + file.filename) # Save the file to a specific directory
        mp3Name = find_mp4('./assets/uploads','./assets/mp3')
        return jsonify({'data':mp3Name,'message': 'File uploaded successfully'})


    def get(self):
        return 'bhen ke lode, post request mar'

api.add_resource(Convert,'/convert')

if __name__ == '__main__':
    app.run(debug=True)