from flask import Flask, request, send_file, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from mp4_to_mp3 import find_mp4
from mp3Clipper import split_mp3
from inference import inference
import os

app = Flask(__name__)
CORS(app, origins='*')
api = Api(app)

def create_dict():
    res = {}
    names = os.listdir("./datasets/imgs")
    names.remove("tmp")
    for i,name in enumerate(names):
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
        inference(os.path.join('models','acc-69.pth'), os.path.join("assets","chunks"), type_map,step)
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


api.add_resource(Convert, '/convert')
api.add_resource(Clear, '/clear')


if __name__ == '__main__':
    app.run(debug=True)
