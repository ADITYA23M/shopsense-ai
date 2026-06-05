from flask import Flask, jsonify, request, send_from_directory
import json
import os

app = Flask(__name__, static_folder='frontend')

# Load all products from your existing JSON
def load_products():
    products = []
    for filename in ['books.json','electronics.json','laptops.json']:
        if os.path.exists(filename):
            with open(filename,'r') as f:
                products += json.load(f)
    return products

# API endpoint to get products
@app.route('/api/products', methods=['GET'])
def get_products():
    query = request.args.get('query','').lower()
    category = request.args.get('category','').lower()
    budget = request.args.get('budget',None)
    preference = request.args.get('preference','').lower()

    try:
        budget = float(budget)
    except:
        budget = None

    products = load_products()
    filtered = []
    for p in products:
        if query and query not in p['name'].lower(): continue
        if category and category != p['category'].lower(): continue
        if budget and p['price']>budget: continue
        if preference and preference not in p['name'].lower(): continue
        filtered.append(p)

    # Sort by rating + reviews
    filtered.sort(key=lambda x: x['rating']+x['reviews']/1000, reverse=True)
    return jsonify(filtered)

# Serve frontend files
@app.route('/', defaults={'path':''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join('frontend',path)):
        return send_from_directory('frontend', path)
    else:
        return send_from_directory('frontend','index.html')

if __name__ == '__main__':
    app.run(debug=True)