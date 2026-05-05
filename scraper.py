import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

url = "https://lblite.lightning-bolt.com/public/659663dc-845e-49b3-b9fd-a11872df3ca1"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Map today's weekday to column (Mon=1, Tue=2, Wed=3, Thu=4, Fri=5, Sat=6, Sun=7)
# Using % 7 + 1 handles edge cases for weekend transitions
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
    if len(cols) < 2: continue # Skip empty rows
    
    # Get the text from the first column (the role/assignment name)
    # Using 'contains' logic to be safer
    assignment_name = cols[0].get_text(strip=True)
    
    for key, label in targets.items():
        if key in assignment_name:
            # Grab the name from the correct day column
            try:
                name = cols[weekday_col].get_text(strip=True)
                if "PA" in key:
                    results["PAs"].append({"role": label, "name": name})
                else:
                    results[label] = name
            except IndexError:
                continue

# Save the data
with open('data.json', 'w') as f:
    json.dump(results, f)
