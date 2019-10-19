import requests
import json


headers = {
    'organizationid': "3ae6bd8b-23b6-47c7-a9a0-8dc56833ca18",
    'secretkey': "7ab90651-f1c6-4756-a980-3813bf682198",
}

payload_info = {"name": 'Test',
                "description": 'Test',
                "coreLanguage": "en-US"}

data = json.dumps(payload_info)

resp = requests.post('https://api.genesysappliedresearch.com/v2/knowledge/generatetoken', headers=headers, data=data)

print(resp.json())
