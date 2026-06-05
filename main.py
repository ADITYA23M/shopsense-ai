# main.py
from product_api import search_products

def display_comparison(selected_products):
    print("\n📊 Product Comparison:\n")
    print(f"{'Name':40} | {'Category':12} | {'Price':7} | {'Rating':6} | {'Reviews':7} | {'Source':10}")
    print("-" * 100)
    for p in selected_products:
        print(f"{p['name'][:40]:40} | {p['category']:12} | ${p['price']:6} | {p['rating']:6} | {p['reviews']:7} | {p['source']:10}")
    print("-" * 100 + "\n")

def main():
    print("🛒 Welcome to Smart Shopping Assistant!\n")

    query = input("What do you want to buy? ").strip()
    category = input("Category (book/smartphone/laptop/leave blank for all): ").strip()
    budget_input = input("Enter your budget (optional): ").strip()
    preference = input("What matters most? (optional): ").strip()

    budget = float(budget_input) if budget_input else None

    print("\n🔎 Searching for products, please wait...\n")
    results = search_products(query, category=category, budget=budget, preference=preference)

    if not results:
        print("❌ No products found.")
        return

    print(f"✅ Found {len(results)} products:\n")
    for idx, p in enumerate(results, start=1):
        print(f"{idx}. {p['name']} ({p['category']}) - ${p['price']} - Rating: {p['rating']} - Reviews: {p['reviews']} - Source: {p['source']}")

    # Ask user to select products for comparison
    print("\nSelect up to 3 products to compare (enter numbers separated by commas, e.g., 1,3):")
    choices_input = input().strip()
    choices = [int(x)-1 for x in choices_input.split(",") if x.isdigit()]
    selected_products = [results[i] for i in choices if 0 <= i < len(results)]

    if not selected_products:
        print("\n❌ No products selected for comparison.")
        return

    # Sort option
    print("\nSort comparison by (enter number):\n1. Price\n2. Rating\n3. Reviews\nLeave blank for default (Rating+Reviews)")
    sort_choice = input().strip()

    if sort_choice == "1":
        selected_products.sort(key=lambda x: x["price"])
    elif sort_choice == "2":
        selected_products.sort(key=lambda x: x["rating"], reverse=True)
    elif sort_choice == "3":
        selected_products.sort(key=lambda x: x["reviews"], reverse=True)
    else:
        selected_products.sort(key=lambda x: (x["rating"], x["reviews"]), reverse=True)

    # Display comparison
    display_comparison(selected_products)

if __name__ == "__main__":
    main()