

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mydjango.settings'
import django
django.setup()
import requests
from graphqlendpoint.models import Agent


users = []
url = 'http://ot-ws:5000/api/ot/objects'
payload = '{"objectclass": "Agent", "filter": "", "variables": [], "requiredfields": [] }'

req = requests.post(url, payload, headers={"Content-Type": "application/json"})

print(requests)

agents = Agent.objects.all()

# sid=response.json()['Object']['login']['sessionId']
