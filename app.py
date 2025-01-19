# app.py
from flask import Flask, jsonify
from flask_pymongo import PyMongo

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)