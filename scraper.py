import json
from datetime import datetime
from playwright.sync_api import sync_playwright

url = "https://1blite.lightning-bolt.com/public/659663dc-845e-49b3-b9fd-a11872df3ca1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print(f"Loading {url}...")
    page.goto(url, wait_until="networkidle", timeout=60000)

    # Wait extra for JS to render
    page.wait_for_timeout(5000)

    # Print the full HTML so we can see the structure
    html = page.content()
    print("=== PAGE HTML (first 5000 chars) ===")
    print(html[:5000])
    print("=== END HTML ===")

    # Also print all visible text
    print("=== VISIBLE TEXT ===")
    text = page.inner_text("body")
    print(text[:3000])
    print("=== END TEXT ===")

    browser.close()

# Write empty data.json so site doesn't break
with open("data.json", "w") as f:
    json.dump({"PAs": []}, f, indent=2)
