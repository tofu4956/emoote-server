from graphene.types import datetime
from userdatas.models import Entry, Userdata
import graphene
import datetime
from graphene_django import DjangoObjectType
from django.test import TestCase

# Create your tests here.

class UserdataNode(DjangoObjectType):
    class Meta:
        model = Userdata
        
class EntryNode(DjangoObjectType):
    class Meta:
        model = Entry
        
class Query(graphene.ObjectType):
    users = graphene.List(UserdataNode)
    user = graphene.Field(UserdataNode, id=graphene.Int())
    entry = graphene.List(EntryNode, id=graphene.Int())
    