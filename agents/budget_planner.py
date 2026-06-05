# agents/budget_planner.py
from crewai import Agent

def create_budget_planner(api_key=None, budget=None):
    def filter_budget(products):
        if budget is None:
            return products
        return [p for p in products if p["price"] <= budget]
    
    return Agent(
        name="Budget Planner",
        description=f"Filters products under budget {budget}",
        execute=filter_budget
    )