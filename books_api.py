# books_api.py
import requests
import json
import os
import time

CACHE_FILE = "books_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def search_books(query, max_results=20):
    """
    Search books using Open Library API.
    Uses local cache to avoid repeated requests.
    Returns a list of books with title, author, and year.
    """
    query_lower = query.lower()
    cache = load_cache()
    if query_lower in cache:
        return cache[query_lower]

    url = f"https://openlibrary.org/search.json?q={query}"
    attempts = 3
    for i in range(attempts):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            books = []
            for doc in data.get("docs", [])[:max_results]:
                books.append({
                    "title": doc.get("title", "Unknown"),
                    "author": ", ".join(doc.get("author_name", ["Unknown"])),
                    "year": doc.get("first_publish_year", "Unknown")
                })
            # Save to cache
            cache[query_lower] = books
            save_cache(cache)
            return books
        except requests.RequestException as e:
            print(f"❌ Attempt {i+1} failed: {e}")
            if i < attempts - 1:
                print("⏳ Retrying...")
                time.sleep(3)
            else:
                print("❌ Could not fetch books after 3 attempts. Using cache if available.")
                return cache.get(query_lower, [])