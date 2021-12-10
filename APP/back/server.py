from flask import Flask, request, Response, jsonify
from flask_cors import CORS, cross_origin
from webmToWav import convertWebm
import time

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app, resources={r'*': {'origins': '*'}})

@app.route('/process-register', methods=['POST'])
def process_register():
    
    json = request.get_json() 

    convertWebm( json["path"] , json["fieldname"])
    print( json["path"] , json["fieldname"] , "\n")

    #time.sleep(20)

    data = {'status':'registered', 'name':'kyu'}
    return jsonify(data), 200

@app.route('/process-diary', methods=['POST'])
def process_diary():
    
    json = request.get_json() 

    convertWebm( json["path"] , json["fieldname"])
    print( json["path"] , json["fieldname"] , "\n")

    #time.sleep(20)

    data = {'emotion': 'converted', 'text' : 'this is diary'}
    return jsonify(data), 200

app.run(port=8080)