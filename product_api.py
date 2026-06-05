# product_api.py
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_cache(filename):
    path = os.path.join(BASE_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Load all caches
ALL_PRODUCTS = {
    "book": load_cache("books.json"),
    "smartphone": load_cache("electronics.json"),
    "laptop": load_cache("laptops.json")
}

def search_products(query, category=None, max_results=20, budget=None, preference=None):
    query = query.lower()
    results = []

    for key, products in ALL_PRODUCTS.items():
        for p in products:
            name_lower = p["name"].lower()
            category_lower = p["category"].lower()

            # Match either query in name OR category
            if query not in name_lower and query != category_lower:
                continue

            # Category filter
            if category and category.lower() != category_lower:
                continue

            # Budget filter
            if budget and p["price"] > budget:
                continue

            # Preference filter (check anywhere in name)
            if preference and preference.lower() not in name_lower:
                continue

            results.append(p)

    # Sort by rating then reviews
    results.sort(key=lambda x: (x["rating"], x["reviews"]), reverse=True)
    return results[:max_results]