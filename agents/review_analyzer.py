# agents/review_analyzer.py
from crewai import Agent

def create_review_analyzer(api_key=None):
    def analyze_reviews(products):
        # Add a simple rating analysis; in real project, call Gemini/OpenAI
        for p in products:
            p["score"] = p.get("rating", 0) * 0.7 + (20000 - p["price"])/20000 * 0.3
        return sorted(products, key=lambda x: x["score"], reverse=True)
    
    return Agent(
        name="Review Analyzer",
        description="Analyzes reviews and score for products",
        execute=analyze_reviews
    )