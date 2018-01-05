
from flask_restplus import fields
from ot_ws.api.restplus import api

event = api.model('Event:', {
    'UCID': fields.String(description='call id from phone system'),
    'start': fields.DateTime,
    'end': fields.DateTime,
    'Applicant' : fields.String('login name from an agent'),
    'State' : fields.String('a state')
})

ticket = api.model('Ticket:', {
    'title': fields.String(description='ticket title'),
    'description': fields.String(),
    'category': fields.Integer(description='id from a category'),
    'Applicant' : fields.String('login name from an agent'),
    'Responsible' : fields.String('login name from an agent'),
    'State' : fields.String('a state')
})

