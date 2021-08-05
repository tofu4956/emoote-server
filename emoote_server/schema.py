import graphene

from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import relay
import userdatas.schema



class Query(userdatas.schema.Query, graphene.ObjectType):
    pass

class Mutation(userdatas.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)