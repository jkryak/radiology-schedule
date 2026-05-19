import json
from datetime import datetime
from playwright.sync_api import sync_playwright

url = "https://1blite.lightning-bolt.com/public/659663dc-845e-49b3-b9fd-a11872df3ca1"

today_str = datetime.now().strftime("%m/%d").lstrip("0").replace("/0", "/")  # e.g. "5/19"
today_str_padded = datetime.now().strftime("%m/%d")  # e.g. "05/19"

# Search terms — keys are substrings to find in row labels, values are output labels
doctor_targets = {
    "IR 4553151": "IR Primary",
    "IR Assist": "IR Assist",
    "IR/CT": "IR/CT",
}

pa_targets = {
    "PA IR Outpatient": "IR Outpatient",
    "PA CT": "CT",
    "PA IR Inpatient 1": "Inpatient 1",
    "PA GOR": "GOR",
    "PA GWH FL 1": "GWH FL 1",
}

results = {"PAs": []}

def find_target_column(headers):
    """Find which column index corresponds to today's date."""
    for idx, header in enumerate(headers):
        text = header.strip()
        if today_str in text or today_str_padded in text:
            return idx
    # Fallback to weekday (Mon=1, Tue=2, ...)
    return datetime.now().weekday() + 1

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    print(f"Loading {url}...")
    page.goto(url, wait_until="networkidle", timeout=60000)

    # Wait for table to appear
    try:
        page.wait_for_selector("table", timeout=30000)
        print("Table found.")
    except Exception as e:
        print(f"Table not found: {e}")
        browser.close()
        with open("data.json", "w") as f:
            json.dump(results, f, indent=2)
        exit()

    # Get all rows
    rows = page.query_selector_all("tr")
    print(f"Found {len(rows)} rows")

    target_column = None

    for row in rows:
        cells = row.query_selector_all("td, th")
        if not cells:
            continue

        cell_texts = [c.inner_text().strip() for c in cells]

        # Detect header row containing today's date
        if target_column is None:
            for idx, text in enumerate(cell_texts):
                if today_str in text or today_str_padded in text:
                    target_column = idx
                    print(f"Found today's column at index {idx}: '{text}'")
                    break

        if target_column is None or len(cell_texts) <= target_column:
            continue

        row_label = cell_texts[0]
        name_found = cell_texts[target_column]

        # Check for doctors
        for key, display_label in doctor_targets.items():
            if key in row_label:
                results[display_label] = name_found
                print(f"Doctor match: {display_label} = {name_found}")

        # Check for PAs
        for key, display_label in pa_targets.items():
            if key in row_label:
                results["PAs"].append({"role": display_label, "name": name_found})
                print(f"PA match: {display_label} = {name_found}")

    # If column still not found, fallback
    if target_column is None:
        target_column = datetime.now().weekday() + 1
        print(f"Date not found in headers, falling back to weekday column {target_column}")

    browser.close()

print(f"Final results: {results}")

with open("data.json", "w") as f:
    json.dump(results, f, indent=2)

print("data.json written successfully.")
