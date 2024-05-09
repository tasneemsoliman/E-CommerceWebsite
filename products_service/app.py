from flask import Flask, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
MONGO_HOST = "productdb"
MONGO_PORT = 27017
MONGO_DBNAME = "productdb"
MONGO_COLLECTION = "products"

CORS(app, resources={r"/*": {"origins": "*"}})


# MongoDB connection
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DBNAME]
products_collection = db[MONGO_COLLECTION]

@app.route('/api/products', methods=['GET'])
def get_products():
    products = list(products_collection.find({}, {'_id': 0}))  # Exclude _id field
    return jsonify(products)

@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        # Convert product_id to integer
        product_id = int(product_id)

        # Find the document containing the product data matching the given ID
        product = products_collection.find_one({"id": product_id})

        if product:
            # Remove the MongoDB ObjectId from the product data
            product.pop('_id', None)
            return jsonify({'success': True, 'data': product}), 200
        else:
            return jsonify({'success': False, 'error': 'Product not found'}), 404

    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid product ID'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
