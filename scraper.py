import requests
from bs4 import BeautifulSoup

url = "https://lblite.lightning-bolt.com/public/659663dc-845e-49b3-b9fd-a11872df3ca1"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# The assignments you actually care about
targets = [
    "IR 4553151", "IR Assist", "IR/CT 4554653", 
    "PA IR Outpatient", "PA CT", "PA IR Inpatient 1", "PA GOR", "PA GMH FL 1"
]

schedule_data = {}

rows = soup.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    if not cols: continue
    
    assignment_name = cols[0].get_text(strip=True)
    
    if assignment_name in targets:
        # Extract Mon-Sun names (columns 1 through 7)
        days = [c.get_text(strip=True) for c in cols[1:8]]
        schedule_data[assignment_name] = days

# Now you have a clean dictionary to display on your own website
