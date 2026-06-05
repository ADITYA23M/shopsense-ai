import streamlit as st
import os
from crewai_tools import SerpApiGoogleShoppingTool

# API KEY (PUT YOUR REAL KEY HERE)
os.environ["SERPAPI_API_KEY"] = "bed718971b8915184205b2ec64e872d8ff41d197a3726df191afe8a879f03ae5"

tool = SerpApiGoogleShoppingTool()

st.set_page_config(page_title="ShopSense AI", layout="wide")

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Filters")

budget = st.sidebar.slider("💰 Max Budget", 0, 200000, 50000)
min_rating = st.sidebar.slider("⭐ Minimum Rating", 0.0, 5.0, 4.0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Tips")
st.sidebar.write("Search like:")
st.sidebar.write("- iPhone 15")
st.sidebar.write("- Gaming Laptop")
st.sidebar.write("- Wireless Earbuds")

# ---------------- MAIN ----------------
st.title("🛒 ShopSense AI")
st.markdown("### Smart Shopping Assistant 🤖")

query = st.text_input("🔍 Search Products")
compare_ids = st.text_input("⚖️ Compare (e.g. 1,2,3)")

# ---------------- SEARCH ----------------
if st.button("Search") and query:

    with st.spinner("🔎 Fetching real products..."):
        results = tool.run(search_query=query)

    # Handle response
    if isinstance(results, dict):
        items = results.get("shopping_results", [])
    elif isinstance(results, list):
        items = results
    else:
        st.write(results)
        items = []

    # ---------------- FILTER ----------------
    filtered = []
    for item in items:
        price = item.get("price", "")
        rating = float(item.get("rating", 4.5))

        try:
            price_val = int(''.join(filter(str.isdigit, price)))
        except:
            price_val = 0

        if price_val <= budget and rating >= min_rating:
            item["price_val"] = price_val
            filtered.append(item)

    if not filtered:
        st.error("❌ No products match your filters")
    else:
        st.success(f"✅ {len(filtered)} products found")

        # ---------------- AI RECOMMENDATION ----------------
        st.subheader("🤖 Smart Picks")

        best = sorted(filtered, key=lambda x: x["price_val"])[:3]

        for p in best:
            st.write(f"👉 **{p.get('title')}** — Best value under your budget")

        # ---------------- PRODUCT GRID ----------------
        st.subheader("🛍️ Products")

        cols = st.columns(3)

        for i, item in enumerate(filtered[:9]):
            with cols[i % 3]:
                st.image(item.get("thumbnail", "https://via.placeholder.com/150"))
                st.markdown(f"**{i+1}. {item.get('title')}**")
                st.write(f"💰 {item.get('price')}")
                st.write(f"⭐ {item.get('rating', '4.5')}")
                st.markdown(f"[View Product]({item.get('link','#')})")

        # ---------------- COMPARISON ----------------
        if compare_ids:
            st.subheader("⚖️ Comparison")

            try:
                ids = [int(x.strip()) - 1 for x in compare_ids.split(",")]
                selected = [filtered[i] for i in ids if i < len(filtered)]

                for item in selected:
                    st.write(f"### {item.get('title')}")
                    st.write(f"💰 Price: {item.get('price')}")
                    st.write(f"⭐ Rating: {item.get('rating')}")
                    st.write("---")

            except:
                st.error("Invalid comparison input")

# ---------------- CHAT ----------------
st.subheader("💬 Assistant")

user_msg = st.text_input("Ask something (e.g. best phone under 30000)")

if user_msg:
    st.write("🤖 Suggestion:")
    st.write(f"Try searching: **{user_msg}** above 👆")