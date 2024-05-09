from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# MongoDB configuration for cart and orders
CART_MONGO_HOST = "cartdb"  # Name of the MongoDB container for cart
CART_MONGO_PORT = 27017
CART_MONGO_DBNAME = "cartdb"  # Name of the database for cart
CART_MONGO_COLLECTION = "cart"  # Name of the collection for cart

ORDERS_MONGO_HOST = "ordersdb"  # Name of the MongoDB container for orders
ORDERS_MONGO_PORT = 27017
ORDERS_MONGO_DBNAME = "ordersdb"  # Name of the database for orders
ORDERS_MONGO_COLLECTION = "orders"  # Name of the collection for orders

# Initialize MongoDB clients for cart and orders
cart_client = MongoClient(CART_MONGO_HOST, CART_MONGO_PORT)
orders_client = MongoClient(ORDERS_MONGO_HOST, ORDERS_MONGO_PORT)

# Select the databases and collections
cart_db = cart_client[CART_MONGO_DBNAME]
orders_db = orders_client[ORDERS_MONGO_DBNAME]
cart_collection = cart_db[CART_MONGO_COLLECTION]
orders_collection = orders_db[ORDERS_MONGO_COLLECTION]

@app.route('/cart/<user_id>', methods=['GET'])
def get_products_from_cart(user_id):
    try:
        cart = cart_collection.find_one({"userId": user_id})
        if cart:
            cart["_id"] = str(cart["_id"])
            return jsonify({'success': True, 'data': cart}), 200
        else:
            return jsonify({'success': False, 'error': 'Cart not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/cart', methods=['POST'])
def add_products_to_cart():
    try:
        cart_data = request.json
        if not cart_data or 'userId' not in cart_data or 'productId' not in cart_data:
            return jsonify({'success': False, 'error': 'Invalid cart data'}), 400

        user_id = cart_data['userId']
        product_id = cart_data['productId']

        # Check if the user's cart exists
        cart = cart_collection.find_one({"userId": user_id})

        if cart:
            # If the cart exists, append the new product ID to the existing cart items
            cart_collection.update_one({"userId": user_id}, {"$addToSet": {'productIds': product_id}})
        else:
            # If the cart doesn't exist, create a new cart with the new product ID
            cart_collection.insert_one({"userId": user_id, "productIds": [product_id]})

        return jsonify({'success': True, 'message': 'Product added to cart!'}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/checkout/<user_id>', methods=['POST'])
def checkout(user_id):
    try:
        cart = cart_collection.find_one({"userId": user_id})
        if not cart:
            return jsonify({'success': False, 'error': 'Cart not found for checkout'}), 404

        # Insert cart items into orders collection
        orders_collection.insert_one(cart)

        cart_collection.delete_many({"userId": user_id})
        

        return jsonify({'success': True, 'message': 'Checkout successful!'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/')
def check_service_running():
    return 'Hello World! - from shopping cart service.'

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
