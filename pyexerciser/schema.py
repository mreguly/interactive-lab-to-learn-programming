import graphene
from graphene_django.debug import DjangoDebug
import api.schema


class Query(api.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    debug = graphene.Field(DjangoDebug, name='__debug')

schema = graphene.Schema(query=Query)