import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

url = "https://lblite.lightning-bolt.com/public/659663dc-845e-49b3-b9fd-a11872df3ca1"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Get today's date in MM/DD format (e.g., "05/05")
today_str = datetime.now().strftime("%m/%d")

targets = {
    "IR 4553151": "IR Primary",
    "IR Assist": "IR Assist",
    "IR/CT 4554653": "IR/CT",
    "PA IR Outpatient": "IR Outpatient",
    "PA CT": "CT",
    "PA IR Inpatient 1": "Inpatient 1",
    "PA GOR": "GOR",
    "PA GMH FL 1": "GMH FL 1"
}

results = {"PAs": []}
target_column = None

# Find all table rows
rows = soup.find_all('tr')

# 1. FIND THE CORRECT COLUMN FOR TODAY
for row in rows:
    header_cols = row.find_all(['th', 'td'])
    for idx, col in enumerate(header_cols):
        if today_str in col.get_text():
            target_column = idx
            break
    if target_column:
        break

# Default to current weekday index if date search fails
if not target_column:
    target_column = datetime.now().weekday() + 1

# 2. EXTRACT DATA FROM THAT COLUMN
for row in rows:
    cols = row.find_all('td')
    if len(cols) <= target_column: continue
    
    assignment_text = cols[0].get_text(strip=True)
    
    for key, label in targets.items():
        if key in assignment_text:
            name = cols[target_column].get_text(strip=True)
            if "PA" in key:
                results["PAs"].append({"role": label, "name": name})
            else:
                results[label] = name

# Save to data.json
with open('data.json', 'w') as f:
    json.dump(results, f)
