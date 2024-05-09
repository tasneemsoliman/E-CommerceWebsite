from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# MongoDB configuration
MONGO_HOST = "ordersdb"  
MONGO_PORT = 27017

# Initialize MongoDB client
client = MongoClient(MONGO_HOST, MONGO_PORT)

db = client['ordersdb']
orders_collection = db['orders']

@app.route('/api/orders/<user_id>', methods=['GET'])
def get_orders(user_id):
    orders = list(orders_collection.find({"userId": user_id}, {'_id': 0}))  # Exclude _id field
    return jsonify(orders)


# @app.route('/api/orders/<order_id>', methods=['GET'])
# def get_order(order_id):
#     try:
#         # Convert order_id to ObjectId
#         order_id_obj = ObjectId(order_id)
        
#         # Query the database using the ObjectId
#         order = orders_collection.find_one({'_id': order_id_obj}, {'_id': 0})
        
#         # Check if order exists
#         if order:
#             return jsonify(order)
#         else:
#             return jsonify({"error": "Order not found"}), 404
#     except Exception as e:
#         return jsonify({"error": str(e)}), 400  # Return error if order_id is invalid

@app.route('/api/', methods=['GET'])
def hello():
    return 'Hello from Order Service!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
