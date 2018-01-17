import graphene
from graphene import relay, ObjectType, AbstractType
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import datetime

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
        filter_fields = ['ucid', 'origin','destination','state', 'start', 'end', 'isContactCenterCall']
        interfaces = (relay.Node,)


class EventNode(DjangoObjectType):
    class Meta:
        model = Event
        filter_fields = ['ot_id', 'applicant','phone', 'end']
        interfaces = (relay.Node,)


class QueryCalls(object):
    calls = relay.Node.Field(CallNode)
    all_calls = DjangoFilterConnectionField(CallNode)

class QueryTodayCalls(object):
    calls = relay.Node.Field(CallNode)

    def resolve_today(self, info, **kwargs):
        today = Call.objects.filter(start__gte=datetime.datetime.today() - datetime.timedelta(hours=12)).filter(
            isContactCenterCall=True)
        return today





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


