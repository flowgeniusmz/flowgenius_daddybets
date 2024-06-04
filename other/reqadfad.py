import requests
import json

respons=requests.get(url="https://sportsbook-nash-usil.draftkings.com/sites/US-IL-SB/api/v5/eventgroups/92483?format=json", headers={"Content-Type": "application/json"})
adsf = respons.json()
print(adsf)