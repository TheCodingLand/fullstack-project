

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

data = req.json()

agents = Agent.objects.all()


print(data['status'])
for agent in data['Agent']:
    id = agent['id']
    firstname = agent['data']['FirstName']
    lastname = agent['data']['LastName']
    phone = '%s' % agent['data']['Phone']
    login = agent['data']['Login Name']
    displayname = agent['data']['Title']
    email = agent['data']['Email Address']
    phone = phone[1:]
    print(phone)
    for a in agents:
        if a.ext == phone:
            a.firstname = firstname
            a.lastname = lastname
            a.ot_id = id
            a.email = email
            a.ot_userdisplayname = displayname
            a.ot_userloginname = login
            a.save()
            print("%s - %s - %s - %s - %s - %s - %s" %
                  (id, firstname, lastname, phone[1:], login, displayname, email))

