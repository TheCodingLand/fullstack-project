
from flask_restplus import fields
from ot_ws.api.restplus import api

event = api.model('Event:', {
    'UCID': fields.String(description='call id from phone system'),
    'CreationDate': fields.DateTime(),
    'Call Finished Date': fields.DateTime(),
    'Applicant': fields.String('login name from an agent'),
    'Responsible': fields.String('login name from an agent'),
    'State': fields.String('a state'),
    'RelatedIncident': fields.Integer(description='id from a ticket'),
})

ticket = api.model('Ticket:', {
    'Title': fields.String(description='ticket title'),
    'Description': fields.String(),
    'AssociatedCategory': fields.Integer(description='id from a category'),
    'Applicant': fields.String('login name from an agent'),
    'Responsible': fields.String('login name from an agent'),
    'State': fields.String('a state'),
    'SolutionDescription': fields.String('a solution')
})

user = api.model('User:', {
    'FirstName': fields.String(),
    'LastName': fields.String(),
    'Phone': fields.Integer(),
    'Login Name': fields.String(),
    'Email Address': fields.String(),
})

category = api.model('Category', {
    'Title': fields.String(),
    'Predecessor': fields.String(),
    'SearchCode': fields.Integer(),
})

variablelist = api.model("variablelist", {
    'name': fields.String('variable name'),
    'value': fields.String('variable value'),
})

genericfilter = api.model('GenericFilter:', {
    'objectclass': fields.String(description='object class as known in the ot API models.py file'),
    'filter': fields.String(description='the filter name as defined in omnitracker'),
    'variables': fields.List(fields.Nested(variablelist)),
    'requiredfields': fields.List(fields.String(description='fields to return')),
})

GetWithFields = api.model('GetWithFields:', {
    'objectclass': fields.String(description='object class as known in the ot API models.py file'),
    'requiredfields': fields.List(fields.String(description='fields to return')),
})
