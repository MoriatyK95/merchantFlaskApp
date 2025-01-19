# app.py
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import ObjectId

app = Flask(__name__)

# Configuration for MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/marketplaceDB"
mongo = PyMongo(app)



@app.route('/')
def home():
    """
    Home route that returns a simple greeting message.
    """
    return "Hello, Flask!"

@app.route('/users', methods=['GET'])
def get_users():
    """
    GET method to retrieve all users from the MongoDB collection.
    Converts ObjectId to string for JSON serialization.
    Returns a JSON response with a list of users and a 200 status code.
    """
    users = mongo.db.users.find()
    users_list = []
    for user in users:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
        users_list.append(user)
    return jsonify(users_list), 200

@app.route('/users', methods=['POST'])
def create_user():
    """
    POST method to create a new user in the MongoDB collection.
    Expects JSON data with 'username', 'email', and 'role' fields.
    Returns a JSON response with the created user's ID and a 201 status code.
    """
    data = request.get_json()
    if not data or not 'username' in data or not 'email' in data or not 'role' in data:
        return jsonify({"error": "Invalid input"}), 400

    new_user = {
        "username": data['username'],
        "email": data['email'],
        "role": data['role']
    }
    result = mongo.db.users.insert_one(new_user)
    new_user_id = str(result.inserted_id)
    return jsonify({"_id": new_user_id}), 201

@app.route('/user', methods=['GET'])
def get_user():
    """
    GET method to retrieve a user by email or userId from the MongoDB collection.
    Accepts 'email' or user's 'objectID' as query parameters.
    Returns a JSON response with the user data and a 200 status code if found,
    or a 404 status code if not found.
    """
    email = request.args.get('email')
    user_id = request.args.get('userId')

    if email:
        user = mongo.db.users.find_one({"email": email})
    elif user_id:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    else:
        return jsonify({"error": "Invalid query parameters"}), 400

    if user:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)