import graphene
from graphene import relay, ObjectType, AbstractType
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Call, Agent, Event, Ticket, Category


class TicketNode(DjangoObjectType):
    class Meta:
        model = Ticket
        filter_fields = ['title', 'state','solution','responsible','ot_id']
        interfaces = (relay.Node,)

class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['title', 'searchcode','ot_id']
        interfaces = (relay.Node,)
        
        
class AgentNode(DjangoObjectType):
    class Meta:
        model = Agent
        filter_fields = ['firstname', 'lastname', 'ext', 'phone_state','phone_active', 'phone_login']
        interfaces = (relay.Node,)


class CallNode(DjangoObjectType):
    class Meta:
        model = Call
        filter_fields = ['ucid', 'origin','destination','state', 'start', 'end', 'IsContactCenterCall']
        interfaces = (relay.Node,)


class EventNode(DjangoObjectType):
    class Meta:
        model = Event
        filter_fields = ['ot_id', 'applicant','phone', 'end']
        interfaces = (relay.Node,)


class QueryCalls(object):
    calls = relay.Node.Field(CallNode)
    all_calls = DjangoFilterConnectionField(CallNode)


class QueryCategorys(object):
    categorys = relay.Node.Field(CategoryNode)
    all_categorys = DjangoFilterConnectionField(CategoryNode)

class QueryAgents(object):
    agents = graphene.List(AgentNode)
    all_agents = DjangoFilterConnectionField(AgentNode)
        


class QueryEvents(object):
    agents = graphene.List(EventNode)
    all_events = DjangoFilterConnectionField(EventNode)



class QueryTickets(object):
    agents = graphene.List(TicketNode)
    all_agents = DjangoFilterConnectionField(TicketNode)


