import json
from project.models import Ticket
import requests

t = Ticket()
t.Title="ticket"
t.Description="ticket"

url = 'https://api.github.com/some/endpoint' # custom url
payload = {'some': 'data'}
headers = {'content-type': 'application/json'}

def createTicket(ticket):
    r = requests.post(url, data=json.dumps(t.serialize()), headers=headers)

print(json.dumps(t.serialize())) # Just to see the data
  
createTicket(t))
