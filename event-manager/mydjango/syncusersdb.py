

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mydjango.settings'
import django
django.setup()

from graphqlendpoint.models import Agent


users = []
url = 'http://ot-ws:5000/api/ot/'
payload = {
    "objectclass": "Agent",
    "filter": "",
    "variables":
    []}

req = requests.post(url, payload)

print(requests)

agents = Agents.objects.all()

for item in req:
    print("%s" % item)
