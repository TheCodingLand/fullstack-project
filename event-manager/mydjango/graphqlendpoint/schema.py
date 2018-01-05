import graphene
from graphene import relay, ObjectType, AbstractType
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Call, Agent


class CallNode(DjangoObjectType):
    class Meta:
        model = Call
        filter_fields = ['ucid', 'origin','destination','state']
        interfaces = (relay.Node,)
        
        
class AgentNode(DjangoObjectType):
    class Meta:
        model = Agent
        filter_fields = ['firstname', 'lastname', 'ext', 'phone_state','phone_active']
        interfaces = (relay.Node,)


class QueryCalls(object):
    calls = relay.Node.Field(CallNode)
    all_calls = DjangoFilterConnectionField(CallNode)


class QueryAgents(object):
    agents = graphene.List(AgentNode)
    all_agents = DjangoFilterConnectionField(AgentNode)
        

   

    


