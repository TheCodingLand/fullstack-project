# project/api/views.py
from flask_restplus import Namespace, Resource, fields
from ot_ws.api.models.apimodels import event, ticket, genericfilter, GetWithFields, ot_object, client
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)

from flask import request

from ot_ws.api.restplus import api
from ot_ws.ot.query_ot import query_ot
from ot_ws.ot.ot_models import Event, Ticket, Category, Generic, Client
from ot_ws.ot.serialize import serialize, test
# these hold our data model folder, fields list, required fields
import time
from ot_ws.ot.ot_field import *


ns = api.namespace('ot/', description='Operations related to OT events')

event_model = Event()
ticket_model = Ticket()
generic_model = Generic()
client_model = Client()

@ns.route('/schema')
class Swagger(Resource):
    def get(self):
        return api.__schema__


@ns.route('/ping')
class SanityCheck(Resource):
    def get(self):
        # log.info(json.dumps(api.__schema__))
        return {
            'status': 'success',
            'message': 'pong!'
        }


@api.response(404, 'object not found.')
@ns.route('/ot_objects/<int:object_id>', methods=['GET'])
class ObjectsMetadata(Resource):
    def get(self, object_id):
        """Get single object details"""
        response_object = {
            'status': 'fail',
            'message': 'Event does not exist'
        }
        try:

            e = query_ot()
            e.get(object_id)

            result = serialize(e.xml_result.decode("utf-8"))
            # log.info(result)

            ot_object = result.results[0].res
            if not ot_object:
                return response_object, 404
            else:
                response_object = {
                    'status': 'success',
                    'id': e.id,
                    'data': ot_object
                }
                return response_object, 200
        except:
            return response_object, 404


@api.response(404, 'object not found.')
@ns.route('/ot_objects/metadata/<int:object_id>', methods=['GET'])
class ObjectsMetadata(Resource):
    def get(self, object_id):
        """Get single event details"""
        response_object = {
            'status': 'fail',
            'message': 'Event does not exist'
        }
        try:
            e = query_ot()
            e.get(object_id)

            result = serialize(e.xml_result.decode("utf-8"))
            # log.info(result)
            ot_object = result.results[0].metadata
            if not ot_object:
                return response_object, 404
            else:
                response_object = {
                    'status': 'success',
                    'id': e.id,
                    'data': ot_object
                }
                return response_object, 200
        except:
            return response_object, 404


def getFields(object_model, data):
    """Creates ot_field instance so the apo knows how to send it to the original API
    Also serves as validation for returned objects"""
    fields = []
    for key in data.keys():
        if key in object_model.fields.keys():

            cls = globals()[object_model.fields[key]]
            f = cls(key)
            f.value = data[key]
            fields.append(f)
        else:
            log.error("field not in globals")
            raise ValueError('field not in globals')
    return fields




@api.response(400, 'failed.')
@ns.route('/events')
class EventAdd(Resource):
    @api.response(201, 'Event successfully created.')
    @api.expect(event)
    def put(self):
        post_data = request.get_json()

        try:
            fields = getFields(event_model, post_data)
        except:
            response_object = {
                'status': 'fail',
                'message': 'Invalid payload parsing fields.'
            }
            return response_object, 400

        try:
            r = query_ot()

            event = r.add(event_model, fields)
            if event:
                response_object = {
                    'status': 'success',
                    'message': 'event was added!',
                    'event': event
                }

                return response_object, 201
            else:
                logging.error(post_data)
                response_object = {
                    'status': 'fail',
                    'message': 'Sorry. failed.'
                }
                return response_object, 400
        except:
            log.error("faild to createevent with data %s" % post_data)
            response_object = {
                'status': 'fail',
                'message': 'Invalid payload.'
            }
            return response_object, 400


@ns.route('/events/<int:event_id>', methods=['GET'])
class EventItem(Resource):
    def get(self, event_id):
        """Get single event details"""
        response_object = {
            'status': 'fail',
            'message': 'Event does not exist'
        }
        try:
            e = query_ot()
            e.get(event_id)
            #logging.error(e.xml_result.decode("utf-8"))
            result = serialize(e.xml_result.decode("utf-8"))
            id = result.results[0].id
            event = result.results[0].res
            # event = test()
            if not event:
                return response_object, 404

            wrong_type = False
            unexpected_fields = []
            for f in event.keys():
                if f not in event_model.fields:
                    unexpected_fields.append(f)
                    wrong_type = True
            if wrong_type == True:
                response_object = {
                    'status': 'fail',
                    #'message': 'unexpected fields : %s' % (unexpected_fields)
                    'message': 'wrong object returned'
                }
                return response_object, 400
            else:
                response_object = {
                    'status': 'success',
                    'id': id,
                    'data': event
                }
                return response_object, 200
        except IndexError:
            return response_object, 404


@ns.route('/events/ucid/<int:event_ucid>', methods=['GET'])
class EventItemUCID(Resource):
    def get(self, event_ucid):
        """Get single event details"""
        response_object = {
            'status': 'fail',
            'message': 'Event does not exist'
        }
        try:
            e = query_ot()
            e.GetEventByUCID(event_ucid)
            result = serialize(e.xml_result.decode("utf-8"))
            event = result.results[0].res
            id = result.results[0].id
            # event = test()
            if not event:
                return response_object, 404

            wrong_type = False
            unexpected_fields = []
            for f in event.keys():
                if f not in event_model.fields:
                    unexpected_fields.append(f)
                    wrong_type = True
            if wrong_type == True:
                response_object = {
                    'status': 'fail',
                    #'message': 'unexpected fields : %s' % (unexpected_fields)
                    'message': 'wrong object returned'
                }
                return response_object, 400
            else:
                response_object = {
                    'status': 'success',
                    'id': id,
                    'data': event
                }
                return response_object, 200
        except:
            return response_object, 404




@ns.route('/tickets/<int:ticket_id>', methods=['GET'])
class TicketItem(Resource):
    def get(self, ticket_id):
        """Get single ticket details"""
        response_object = {
            'status': 'fail',
            'message': 'Event does not exist'
        }
        try:
            t = query_ot()
            t.get(ticket_id)
            result = serialize(t.xml_result.decode("utf-8")).results[0]
            ticket = result.res
            # event = test()
            if not ticket:
                return response_object, 404

            wrong_type = False
            unexpected_fields = []
            for f in ticket.keys():
                if f not in ticket_model.fields:
                    unexpected_fields.append(f)
                    wrong_type = True
            if wrong_type == True:
                response_object = {
                    'status': 'fail',
                    'message': 'wrong object returned'
                }
                return response_object, 400
            else:
                response_object = {
                    'status': 'success',
                    'data': ticket
                }
                return response_object, 200
        except:
            return response_object, 404


@api.response(400, 'failed.')
@ns.route('/clients')
class TicketAdd(Resource):
    @api.response(201, 'Client successfully created.')
    @api.expect(client)
    def put(self):
        response_object = {
                    'status': 'fail',
                    'message': 'Internal server error.'
                }
        try:
            post_data = request.get_json()

            # log.info(post_data)

            if not post_data:
                response_object = {
                    'status': 'fail',
                    'message': 'Invalid payload.'
                }
            else:

                fields = getFields(client_model, post_data)

                r = query_ot()
                result = r.add(client_model, fields)
                if result:
                    response_object = {
                        'status': 'success',
                        'message': 'client was added!',
                        'ticket': result
                    }
                    return response_object, 201
        
        except:
            return response_object, 500






@api.response(400, 'failed.')
@ns.route('/tickets')
class TicketAdd(Resource):
    @api.response(201, 'Ticket successfully created.')
    @api.expect(ticket)
    def put(self):
        response_object = {
                    'status': 'fail',
                    'message': 'Internal server error.'
                }
        try:
            post_data = request.get_json()

            # log.info(post_data)

            if not post_data:
                response_object = {
                    'status': 'fail',
                    'message': 'Invalid payload.'
                }
            else:

                fields = getFields(ticket_model, post_data)

                r = query_ot()
                result = r.add(ticket_model, fields)
                if result:
                    response_object = {
                        'status': 'success',
                        'message': 'ticket was added!',
                        'ticket': result
                    }
                    return response_object, 201
            
        except:
            return response_object, 500


@api.response(400, 'failed.')
@ns.route('/objects')
class ObjectFilter(Resource):
    @api.response(201, 'list of objects : ok')
    @api.expect(genericfilter)
    def post(self):

        post_data = request.get_json()
        # log.info(request.get_json())
        try:
            r = query_ot()
            # log.info(post_data)

            r.getObjectList(post_data.get(
                'objectclass'), post_data.get('filter'), post_data.get('variables'), post_data.get('requiredfields'))

            items = serialize(r.xml_result.decode("utf-8")).results
            results = []
            for result in items:
                d = {}
                d.update({'id': result.id})
                d.update({'data': result.res})
                results.append(d)

            if results:
                response_object = {
                    'status': 'success',
                    'message': 'object list :',
                    '%s' % post_data.get('objectclass'): results
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Sorry. failed.'
                }
                return response_object, 400
        except:
            response_object = {
                'status': 'fail',
                'message': 'Invalid payload.'
            }
            return response_object, 400


@api.response(400, 'failed.')
@ns.route('/event/<int:event_id>')
class EventMod(Resource):
    @api.response(201, 'object successfully modified.')
    @api.expect(event)
    def put(self, event_id):
        response_object = {
                    'status': 'fail',
                    'message': 'Internal server error.'
                }
        try:

            post_data = request.get_json()
            # log.info(post_data)
            if not post_data:
                response_object = {
                    'status': 'fail',
                    'message': 'Invalid payload.'
                }
            else:
                id = event_id
                fields = getFields(event_model, post_data)
                r = query_ot()
                result = r.modifyObjet(id, fields)
                if result:
                    response_object = {
                        'status': 'success',
                        'message': 'ticket was added!',
                        'ticket': result
                    }
                    return response_object, 201

            response_object = {
                'status': 'fail',
                'message': 'Internal server error.'
            }
        except:
            return response_object, 500



@api.response(400, 'failed.')
@ns.route('/ticket/<int:ticket_id>')
class TicketMod(Resource):
    @api.response(201, 'object successfully modified.')
    @api.expect(ticket)
    def put(self, ticket_id):
        response_object = {
                'status': 'fail',
                'message': 'Invalid payload.'
            }
        try:

            post_data = request.get_json()
            # log.info(post_data)
            if not post_data:
                response_object = {
                    'status': 'fail',
                    'message': 'Invalid payload.'
                }
            else:
                id = ticket_id
                fields = getFields(ticket_model, post_data)
                r = query_ot()
                result = r.modifyObjet(id, fields)
                if result:
                    response_object = {
                        'status': 'success',
                        'message': 'ticket was added!',
                        'ticket': result
                    }
                    return response_object, 201

            response_object = {
                'status': 'fail',
                'message': 'Internal server error.'
            }
        except:
            return response_object, 500




@api.response(400, 'failed.')
@ns.route('/objectmod/<int:object_id>')
class ObjectMod(Resource):
    @api.response(201, 'object successfully modified.')
    @api.expect(ot_object)
    def put(self, object_id):
        response_object = {
            'status': 'fail',
            'message': 'Internal server error.'
        }
        try:

            post_data = request.get_json()
            # log.info(post_data)
            if not post_data:
                response_object = {
                    'status': 'fail',
                    'message': 'Invalid payload.'
                }
            else:
                id = object_id
                fields = getFields(generic_model, post_data)
                r = query_ot()
                result = r.modifyObjet(id, fields)
                if result:
                    response_object = {
                        'status': 'success',
                        'message': 'object was modified!',
                        'object': result
                    }
                    return response_object, 201

            response_object = {
                'status': 'fail',
                'message': 'Internal server error.'
            }
        except:
            return response_object, 500

@api.response(400, 'failed.')
@ns.route('/object/<int:objectid>')
class ObjectFields(Resource):
    @api.response(201, 'object found')
    @api.expect(GetWithFields)
    def post(self, objectid):
        response_object = {
                    'status': 'fail',
                    'message': 'Sorry. failed.'
                }
        try:
            post_data = request.get_json()
            log.error("pulling object %s with field %s" %
                    (objectid, post_data.get('requiredfields')))
            # log.info(request.get_json())
            if True:
                r = query_ot()
                
                r.getWithFields(objectid, post_data.get('requiredfields'))

                logging.error(r.xml_result)

                items = serialize(r.xml_result.decode("utf-8"))
                
                if items.results == []:
                    return response_object, 404
                log.error("pulling object %s with field %s" %
                        (objectid, post_data.get('requiredfields')))
                
                id = items.results[0].id
                data = items.results[0].res

                if data:
                    response_object = {
                        'status': 'success',
                        'message': 'object :',
                        'id': id,
                        'data': data
                    }
                    return response_object, 201
                else:
                    response_object = {
                        'status': 'fail',
                        'message': 'Sorry. failed.'
                    }
                    return response_object, 400
        except:
            return response_object, 500
            # except:
        #     response_object = {
        #         'status': 'fail',
        #         'message': 'Invalid payload.'
        #     }
        #     return response_object, 400