import graphene

import graphqlendpoint.schema




class RootQuery(graphqlendpoint.schema.QueryCategorys,graphqlendpoint.schema.QueryAgents,graphqlendpoint.schema.QueryCalls,graphqlendpoint.schema.QueryEvents,graphqlendpoint.schema.QueryTickets, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

schema = graphene.Schema(query=RootQuery)

