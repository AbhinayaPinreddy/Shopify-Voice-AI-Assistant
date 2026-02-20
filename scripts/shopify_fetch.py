import requests
from bs4 import BeautifulSoup
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# -------------------------
# CONFIG
# -------------------------
STORE_URL = "https://abhinaya-4634.myshopify.com"
STORE_PASSWORD = "Abhi@1234"

# -------------------------
# SESSION (cookie-based)
# -------------------------
session = requests.Session()

def unlock_store():
    """
    Unlocks password-protected Shopify store
    """
    url = f"{STORE_URL}/password"
    payload = {"password": STORE_PASSWORD}
    r = session.post(url, data=payload)
    r.raise_for_status()

def clean_html(html):
    """
    Safely clean HTML -> text
    """
    if not html:
        return ""
    return BeautifulSoup(html, "html.parser").get_text().strip()

def fetch(endpoint):
    """
    Fetch JSON data using unlocked session
    """
    url = f"{STORE_URL}/{endpoint}"
    r = session.get(url)
    r.raise_for_status()
    return r.json()

# -------------------------
# MAIN LOGIC
# -------------------------

# Step 1: Unlock store
unlock_store()

# Step 2: Fetch products
products_raw = fetch("products.json").get("products", [])

products = []
for p in products_raw:
    title = p.get("title", "")
    description = clean_html(p.get("body_html"))
    price = p.get("variants", [{}])[0].get("price", "N/A")

    sizes = list(
        set(
            v.get("option1")
            for v in p.get("variants", [])
            if v.get("option1")
        )
    )

    products.append({
        "type": "product",
        "title": title,
        "content": f"""
Product name: {title}
Price: ₹{price}
Available sizes: {', '.join(sizes) if sizes else 'Not specified'}
Description: {description}
""".strip()
    })


# Step 3: Fetch pages (Shipping, Return, FAQ, etc.)
pages_raw = fetch("pages.json").get("pages", [])

pages = []
for page in pages_raw:
    content = clean_html(page.get("body_html"))
    if content:  # keep only pages with text
        pages.append({
            "type": "page",
            "title": page.get("title", ""),
            "content": content
        })

# Step 4: Save data for RAG
all_data = products + pages

with open(os.path.join(SCRIPT_DIR, "shopify_data.json"), "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print(" Shopify data fetched successfully")
print("Products:", len(products))
print("Pages:", len(pages))
print(" Saved as shopify_data.json")
