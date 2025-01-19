from flask import current_app, jsonify, request
from bson import ObjectId
from . import users_bp


@users_bp.route('/users', methods=['GET'])
def get_users():
    
    db = current_app.mongo.db
    users_collection = db.users
    users = users_collection.find()
    
    users_list = []
    for user in users:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
        users_list.append(user)
    return jsonify(users_list), 200

@users_bp.route('/users', methods=['POST'])
def create_user():
    db = current_app.mongo.db
    users_collection = db.users
    data = request.get_json()
    if not data or not 'username' in data or not 'email' in data or not 'role' in data:
        return jsonify({"error": "Invalid input"}), 400

    new_user = {
        "username": data['username'],
        "email": data['email'],
        "role": data['role']
    }
    result = users_collection.insert_one(new_user)
    new_user_id = str(result.inserted_id)
    return jsonify({"_id": new_user_id}), 201

@users_bp.route('/user', methods=['GET'])
def get_user():
    db = current_app.mongo.db
    users_collection = db.users
    email = request.args.get('email')
    user_id = request.args.get('userId')

    if email:
        user = users_collection.find_one({"email": email})
    elif user_id:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
    else:
        return jsonify({"error": "Invalid query parameters"}), 400

    if user:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404