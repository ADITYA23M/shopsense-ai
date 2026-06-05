# scraper.py
import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "http://books.toscrape.com/catalogue/category/books_1/"

def scrape_products():
    products = []
    page_num = 1

    while True:
        url = f"{BASE_URL}index.html" if page_num == 1 else f"{BASE_URL}page-{page_num}.html"
        response = requests.get(url)
        response.encoding = 'utf-8'
        if response.status_code != 200:
            print(f"Page {page_num} not found. Stopping.")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("article", class_="product_pod")
        print(f"Page {page_num}: Found {len(items)} products")  # debug

        if not items:
            break  # no more products

        for item in items:
            # Product name
            name = item.h3.a["title"]

            # Product price
            price_text = item.find("p", class_="price_color").text
            price_clean = re.sub(r"[^\d.]", "", price_text)
            price = float(price_clean) * 100  # in pence/cents

            # Rating
            rating_class = item.p.get("class", [])
            rating = rating_class[1] if len(rating_class) > 1 else "Not Rated"

            products.append({
                "name": name,
                "price": price,
                "rating": rating
            })

        page_num += 1

    return products

# Quick test
if __name__ == "__main__":
    scraped_products = scrape_products()
    for p in scraped_products:
        print(p)