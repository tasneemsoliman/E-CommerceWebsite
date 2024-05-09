from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# MongoDB configuration
MONGO_HOST = "userdb"  # Name of the MongoDB container
MONGO_PORT = 27017
MONGO_DBNAME = "userdb"  # Name of the database
MONGO_COLLECTION = "users"  # Name of the collection

# Initialize MongoDB client
client = MongoClient(MONGO_HOST, MONGO_PORT)

# Select the database and collection
db = client[MONGO_DBNAME]
collection = db[MONGO_COLLECTION]

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Find user in the MongoDB collection
    user = collection.find_one({'username': username, 'password': password})

    if user:
        # User found, return success response
        user_id = user['_id']  
        return jsonify({'success': True, 'userId': str(user_id)}), 200
    else:
        # User not found or incorrect credentials, return failure response
        return jsonify({'success': False}), 401

@app.route('/api/', methods=['GET'])
def hello():
    return 'Hello from User Service!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
