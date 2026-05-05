import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

url = "https://lblite.lightning-bolt.com/public/659663dc-845e-49b3-b9fd-a11872df3ca1"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 1. FIND THE COLUMN FOR TODAY
# We look for the current day's date (e.g., "05/05")
today_str = datetime.now().strftime("%m/%d")
target_column = None

# Find the header row (usually the first row with 'Assignment')
for row in soup.find_all('tr'):
    cells = row.find_all(['td', 'th'])
    for idx, cell in enumerate(cells):
        if today_str in cell.get_text():
            target_column = idx
            break
    if target_column: break

# Fallback to weekday if date search fails (Mon=1, Tue=2...)
if target_column is None:
    target_column = datetime.now().weekday() + 1

# 2. DEFINE SEARCH TERMS
# We use shorter terms to ensure a match even if there are weird symbols
doctor_targets = {
    "IR 4553151": "IR Primary",
    "IR Assist": "IR Assist",
    "IR/CT": "IR/CT"
}
pa_targets = {
    "PA IR Outpatient": "IR Outpatient",
    "PA CT": "CT",
    "PA IR Inpatient 1": "Inpatient 1",
    "PA GOR": "GOR",
    "PA GMH FL 1": "GMH FL 1"
}

results = {"PAs": []}

# 3. SCRAPE THE DATA
for row in soup.find_all('tr'):
    cols = row.find_all('td')
    if len(cols) <= target_column: continue
    
    row_label = cols[0].get_text(strip=True)
    name_found = cols[target_column].get_text(strip=True)
    
    # Check for Doctors
    for key, display_label in doctor_targets.items():
        if key in row_label:
            results[display_label] = name_found
            
    # Check for PAs
    for key, display_label in pa_targets.items():
        if key in row_label:
            results["PAs"].append({"role": display_label, "name": name_found})

# 4. SAVE DATA
with open('data.json', 'w') as f:
    json.dump(results, f, indent=2)
