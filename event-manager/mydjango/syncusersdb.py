

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

print(req.json())

agents = Agent.objects.all()
print(req['status'])
for agent in req['Agent']:
    print(agent['id'])
    print(agent['data']['FirstName'])
    print(agent['data']['LastName'])
    print(agent['data']['Phone'])


# sid=response.json()['Object']['login']['sessionId']
# docker exec -it  project_event-manager_1  python syncusersdb.py
# {
#   "status": "success",
#   "message": "object list :",
#   "events": [
#     {
#       "id": "44620",
#       "data": {
#         "AcademicTitle": "",
#         "Active": "true",
#         "AssociatedCostcenters": null,
#         "Locations": null,
#         "Applicant": "",
#         "AssignToAllLocations": "false",
#         "Attachments": "",
#         "Authentication": "Password Field",
#         "Birthday": "",
#         "BirthdayReminder": "false",
#         "Calendar": "",
#         "Class": "",
#         "AssociatedCIs": null,
#         "Answers": "",
#         "Company": "",
#         "ContainedInGroups": null,
#         "CreationDate": "2005-11-23T21:50:22",
#         "Department": "",
#         "Description": "",
#         "Email Address": "Manager-Config@localhost",
#         "Fax": "",
#         "FirstName": "",
#         "Gender": "",
#         "IdleSince": "",
#         "InternalNumber": "",
#         "LastChange": "2011-09-07T08:34:01",
#         "LastLogin": "",
#         "LastName": "Manager-Config",
#         "LDAP Profile": "",
#         "Locked": "false",
#         "MainCostCenter": "",
#         "Location": "",
#         "MobilePhone": "",
#         "Number": "2",
#         "Password": "",
#         "PersonnelRecord": "",
#         "Phone": "",
#         "Primary Group": "44659",
#         "Priority": "",
#         "Properties": "",
#         "RefOTUser": "Manager-Config",
#         "RelatedEmails": null,
#         "BirthdayRemindDate": "",
#         "Responsible": "MasterData-Staff",
#         "ResubmissionEnabled": "false",
#         "ResubmissionDate": "",
#         "ResubmissionEmail": "",
#         "ResubmissionReason": "",
#         "ResubmissionText": "",
#         "ResubmissionUser": "",
#         "JobTitle": "",
#         "Salutation": "",
#         "State": "New",
#         "Subclass": "",
#         "Superuser": "false",
#         "Title": "Manager-Config",
#         "Login Name": "Manager-Config",
#         "Type": "UserAccount",
#         "IsVIP": "false",
#         "WebGuestPassword": "",
#         "WebGuestUserName": "",
#         "Windows Domain Name": ""
#       }
#     },
#     {
#       "id": "44627",
#       "data": {
#         "AcademicTitle": "",
#         "Active": "true",
#         "AssociatedCostcenter
