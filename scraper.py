import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import pytz

# Set the timezone to Eastern Time (Greenville, SC)
eastern = pytz.timezone('US/Eastern')
now_eastern = datetime.now(eastern)

# Map today's weekday to column (Mo=1, Tu=2, We=3, Th=4, Fr=5, Sa=6, Su=7)
weekday_col = now_eastern.isoweekday()

url = "https://lblite.lightning-bolt.com/public/659663dc-845e-49b3-b9fd-a11872df3ca1"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

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
    
    # Get the text from the first column (the assignment name)
    assignment_name = cols[0].get_text(strip=True)
    
    if assignment_name in targets:
        # Get the name from the column corresponding to today
        try:
            name = cols[weekday_col].get_text(strip=True)
        except IndexError:
            name = "TBD"
            
        mapped_role = targets[assignment_name]
        
        if "PA" in assignment_name:
            results["PAs"].append({"role": mapped_role, "name": name if name else "Not Assigned"})
        else:
            results[mapped_role] = name if name else "Not Assigned"

# Save the real data
with open('data.json', 'w') as f:
    json.dump(results, f)
