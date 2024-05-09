from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Add this line to enable CORS for all routes

# MongoDB configuration
MONGO_HOST = "saledb"
MONGO_PORT = 27017
MONGO_DBNAME = "saledb"
MONGO_COLLECTION = "sales"

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DBNAME]
sales_collection = db[MONGO_COLLECTION]

@app.route('/api/flash-sales', methods=['GET'])
def get_flash_sales():
    flash_sales = list(sales_collection.find({}, {'_id': 0}))
    return jsonify(flash_sales)

@app.route('/api/', methods=['GET'])
def hello():
    return 'Hello from Sale Service!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
