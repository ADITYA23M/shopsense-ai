# agents/price_comparator.py
from crewai import Agent

def create_price_comparator(api_key=None):
    def compare_prices(products):
        return sorted(products, key=lambda x: x["price"])
    
    return Agent(
        name="Price Comparator",
        description="Sorts products from lowest to highest price",
        execute=compare_prices
    )