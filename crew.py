# crew.py

from crewai import Crew, Task
from agents.product_finder import create_product_finder

def create_crew(query, budget=None):
    product_finder = create_product_finder()

    task = Task(
        description=f"Find best products for: {query} under budget {budget}",
        expected_output="List of best products with name, price, rating",
        agent=product_finder   # ✅ THIS LINE FIXES YOUR ERROR
    )

    crew = Crew(
        agents=[product_finder],
        tasks=[task]
    )

    return crew