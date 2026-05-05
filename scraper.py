import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

url = "https://lblite.lightning-bolt.com/public/659663dc-845e-49b3-b9fd-a11872df3ca1"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the column for today (e.g., "Tu 05/05")
today_str = datetime.now().strftime("%m/%d")
headers = [th.get_text(strip=True) for th in soup.find_all('th')]

# Default to today's weekday column if date match fails
weekday_col = datetime.now().weekday() + 1 

for i, h in enumerate(headers):
    if today_str in h:
        weekday_col = i
        break

targets = {
    "¶IR 4553151": "IR Primary",
    "IR Assist": "IR Assist",
    "¶IR/CT 4554653": "IR/CT",
    "PA IR Outpatient": "IR Outpatient",
    "PA CT": "CT",
    "PA IR Inpatient 1": "Inpatient 1",
    "PA GOR": "GOR",
    "PA GMH FL 1": "GMH FL 1"
}

results = {"PAs": []}

rows = soup.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    if not cols: continue
    
    assignment_name = cols[0].get_text(strip=True)
    
    if assignment_name in targets:
        # Check if index is within range
        if len(cols) > weekday_col:
            name = cols[weekday_col].get_text(strip=True)
            mapped_role = targets[assignment_name]
            
            if "PA" in assignment_name:
                results["PAs"].append({"role": mapped_role, "name": name})
            else:
                results[mapped_role] = name

with open('data.json', 'w') as f:
    json.dump(results, f)
