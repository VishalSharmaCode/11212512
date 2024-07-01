from flask import Flask, jsonify, request

app = Flask(__name__)

products = [  # In-memory product data
    {
        'company': 'AMZ',
        'category': 'Phone',
        'name': 'iPhone 13 Pro Max',
        'price': 1099.00
    },
    # ... more products
]

@app.route('/products', methods=['GET'])
def get_products():
    # Filter logic based on query parameters
    company = request.args.get('company')
    category = request.args.get('category')
    min_price_str = request.args.get('minPrice')
    max_price_str = request.args.get('maxPrice')

    # Try converting price strings to floats (handle potential errors)
    try:
        min_price = float(min_price_str) if min_price_str else None
    except ValueError:
        return jsonify({'error': 'Invalid minPrice format'}), 400
    try:
        max_price = float(max_price_str) if max_price_str else None
    except ValueError:
        return jsonify({'error': 'Invalid maxPrice format'}), 400

    filtered_products = [
        product for product in products if (
            (company is None or product['company'] == company) and
            (category is None or product['category'] == category) and
            (min_price is None or product['price'] >= min_price) and
            (max_price is None or product['price'] <= max_price)
        )
    ]

    return jsonify(filtered_products)

if __name__ == '__main__':
    app.run(debug=True)