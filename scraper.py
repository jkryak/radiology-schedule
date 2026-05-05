import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

# 1. ADJUST FOR GREENVILLE TIME (UTC-4)
# GitHub servers run on London time. This ensures 'today' means 'Greenville today'.
now = datetime.utcnow() - timedelta(hours=4)
today_str = now.strftime("%m/%d")
weekday_idx = now.weekday() + 1 # Mon=1, Tue=2...

url = "https://lblite.lightning-bolt.com/public/659663dc-845e-49b3-b9fd-a11872df3ca1"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# These are the exact terms the script looks for in the first column
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
rows = soup.find_all('tr')

# 2. FIND THE COLUMN FOR TODAY'S DATE
target_col = weekday_idx # Default fallback
for row in rows:
    cells = row.find_all(['th', 'td'])
    for i, cell in enumerate(cells):
        if today_str in cell.get_text():
            target_col = i
            break

# 3. EXTRACT THE NAMES
for row in rows:
    cols = row.find_all('td')
    if len(cols) <= target_col: continue
    
    row_label = cols[0].get_text(strip=True)
    
    for key, mapped_label in targets.items():
        if key in row_label:
            name = cols[target_col].get_text(strip=True)
            # If the cell is empty or has a dash, label as "None"
            if not name or name == "-": name = "Not Assigned"
            
            if "PA" in key:
                results["PAs"].append({"role": mapped_label, "name": name})
            else:
                results[mapped_label] = name

# Save to data.json
with open('data.json', 'w') as f:
    json.dump(results, f, indent=2)
