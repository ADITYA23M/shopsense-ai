# agents/product_finder.py

from crewai import Agent

def create_product_finder():
    return Agent(
        name="Product Finder",
        role="Find best products",
        goal="Find best products under budget with good ratings",
        backstory="Expert in finding best deals from e-commerce platforms"
    )