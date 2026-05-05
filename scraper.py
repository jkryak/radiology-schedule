import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

url = "https://lblite.lightning-bolt.com/public/659663dc-845e-49b3-b9fd-a11872df3ca1"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Map today's weekday to the correct column in the table (Mo=1, Tu=2, etc.)
weekday_col = datetime.now().weekday() + 1 

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
for row in rows:
    cols = row.find_all('td')
    if not cols: continue
    
    assignment_name = cols[0].get_text(strip=True)
    
    if assignment_name in targets:
        name = cols[weekday_col].get_text(strip=True)
        mapped_role = targets[assignment_name]
        
        if "PA" in assignment_name:
            results["PAs"].append({"role": mapped_role, "name": name})
        else:
            results[mapped_role] = name

# Save this to a data file
with open('data.json', 'w') as f:
    json.dump(results, f)
