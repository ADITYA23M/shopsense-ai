def match_category(query, category):
    keywords = {
        "phone": ["phone", "mobile", "smartphone"],
        "audio": ["headphone", "earbuds", "audio"]
    }

    for word in keywords.get(category, []):
        if word in query:
            return True
    return False


def filter_products(products, query, budget):
    return [
        p for p in products
        if p["price"] <= budget and match_category(query, p["category"])
    ]


def calculate_score(product, preference, budget):
    score = 0

    # Rating weight
    score += product["rating"] * 3

    # Preference match
    if preference in product["features"]:
        score += 3

    # Budget efficiency
    score += (budget - product["price"]) / 5000

    return score


def rank_products(products, preference, budget):
    return sorted(products, key=lambda p: calculate_score(p, preference, budget), reverse=True)


def explain(product, preference, budget):
    reasons = []

    if preference in product["features"]:
        reasons.append(f"great for {preference}")

    if product["rating"] >= 4.4:
        reasons.append("high rating")

    if product["price"] < budget * 0.8:
        reasons.append("value for money")

    return ", ".join(reasons) if reasons else "balanced choice"