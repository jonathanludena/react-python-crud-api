from flask_cors import CORS
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

app = Flask(__name__)
app.config['MONGO_URI'] = MONGO_URI
mongo = PyMongo(app)

CORS(app)

db = mongo.db.users


@app.route("/")
def index():
    return "<h1>Hola API Flask</h1>"


@app.route("/users", methods=['POST'])
def createUser():
    data = {
        "name": request.json['name'],
        "email": request.json['email'],
        "password": request.json['password']
    }
    print(data)
    id = db.insert_one(data).inserted_id
    return jsonify(str(ObjectId(id)))


@app.route("/users")
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password']
        })
    return jsonify(users)


@app.route("/user/<id>")
def getUser(id):
    user = db.find_one({'_id': ObjectId(id)})
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
        'name': user['name'],
        'email': user['email'],
        'password': user['password']
    })


@app.route("/user/<id>", methods=['DELETE'])
def deleteUser(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'User Deleted'})


@app.route("/user/<id>", methods=['PUT'])
def updateUser(id):
    db.update_one({'_id': ObjectId(id)}, {'$set': {
        'name': request.json['name'],
        'email': request.json['email'],
        'password': request.json['password']
    }})
    return jsonify({
        'message': 'User updated'
    })


if __name__ == "__main__":
    app.run(debug=True)
