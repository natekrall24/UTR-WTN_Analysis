import requests
import json
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font

url = (
    "https://prd-usta-kube-tournamentdesk-public-api.clubspark.pro/"
)


headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json",
}

payload = {
    "query": """
        query TournamentPublicEventData($eventId: ID!, $tournamentId: ID!) {
          tournamentPublicEventData(eventId: $eventId, tournamentId: $tournamentId)
        }
    """,
    "variables": {
        "eventId": "27507F8D-F29A-4901-9EDD-2006418BFF36",
        "tournamentId": "A6A54C3A-A3A3-4FAF-B98F-2E2706DFC7AA",
    },
}

response = requests.post(url, headers=headers, json=payload)

data = response.json()

with open("data.json", "w") as file:
    json.dump(data, file)

roundOneMatchUps = data["data"]["tournamentPublicEventData"]["eventData"]["drawsData"][0]["structures"][0]["roundMatchUps"]["1"]
players_info = []

for matchup in roundOneMatchUps:
    for side in matchup['sides']:
        if side.get('bye', False):
            continue
        person = side['participant']['person']
        first_name = person['standardGivenName']
        last_name = person['standardFamilyName']
        section = next((ext['value']['name'] for ext in person['extensions'] if ext['name'] == 'ustaSection'), None)
        
        players_info.append({
            "First Name": first_name,
            "Last Name": last_name,
            "USTA Section": section
        })

#export to excel
df = pd.DataFrame(players_info)
df['Name'] = df['First Name'].str.lower() + df['Last Name'].str.lower()
df = df[['Name', 'USTA Section']]
df.to_excel('B16_22_Regions.xlsx', index=False, engine='openpyxl')