import os
from crewai_tools import SerpApiGoogleShoppingTool

# Set API key
os.environ["SERPAPI_API_KEY"] = "bed718971b8915184205b2ec64e872d8ff41d197a3726df191afe8a879f03ae5"

tool = SerpApiGoogleShoppingTool()

def run_shopping(query):
    print("\n🔎 Searching...\n")

    try:
        results = tool.run(search_query=query)

        # Case 1: If string → just print
        if isinstance(results, str):
            print(results)
            return

        # Case 2: If dict → extract shopping results
        if isinstance(results, dict):
            items = results.get("shopping_results", [])
        else:
            items = results  # already list

        if not items:
            print("❌ No products found")
            return

        for i, item in enumerate(items[:5], start=1):
            title = item.get("title", "No title")
            price = item.get("price", "N/A")
            link = item.get("link", "")

            print(f"{i}. {title}")
            print(f"   Price: {price}")
            print(f"   Link: {link}\n")

    except Exception as e:
        print("❌ Error:", e)


# IMPORTANT PART
if __name__ == "__main__":
    query = input("What do you want to buy? ")
    run_shopping(query)