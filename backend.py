from flask import Flask, request, send_file, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from mp4_to_mp3 import find_mp4
from mp3Clipper import split_mp3
import os

app = Flask(__name__)
CORS(app, origins='*')
api = Api(app)

class Convert(Resource):
    def post(self):
        file = request.files['uploaded_file']
        file.save('./assets/uploads/' + file.filename)
        mp3_name = find_mp4('./assets/uploads', './assets/mp3')
        split_mp3('./assets/chunks', 10)
        return jsonify({'data': mp3_name, 'message': 'File uploaded successfully'})

api.add_resource(Convert, '/convert')

if __name__ == '__main__':
    app.run(debug=True)
