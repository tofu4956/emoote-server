from datetime import date

from django.contrib.auth import login
import graphene
from graphene import relay
from graphql_auth import relay as relay_auth
from .models import Entry
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required

class EntryType(DjangoObjectType):
    class Meta:
        model = Entry
        
class EntryNode(DjangoObjectType):
    class Meta:
        model = Entry
        filter_fields = ['createdtime', 'entry']
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    all_Entry = graphene.List(EntryType)
    entry = graphene.Field(EntryType,
                           id=graphene.ID(),
                           createdtime=graphene.DateTime(),
                           entry=graphene.String())
    @login_required
    def fetch_all_entry(self,info, **kwargs):
        return Entry.objects.all()
    def fetch_entry(self, info, **kwargs):
        createdtime = kwargs.get('createdtime')
        if createdtime != None:
            return Entry.objects.get(createdtime=createdtime)
        return None
    
class EntryCreateMutation(graphene.Mutation):
    class Arguments:
        createdtime = graphene.Date(required=True)
        entry = graphene.String(required=True)
    entry = graphene.Field(EntryType)
    def mutate(self,info,createdtime,entry):
        entries = Entry.objects.create(id=id,createdtime=createdtime,entry=entry)
        return EntryCreateMutation(entries=entries)
    
class EntryUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        createdtime = graphene.Date(required=True)
        entry = graphene.String()
    entry = graphene.Field(EntryType)
    def mutate(self,info,id,createdtime,entry):
        entries = Entry.objects.get(pk=id)
        entries.save()
        return EntryUpdateMutation(entries=entries)

class EntryDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    entry = graphene.Field(EntryType)
    def mutate(self,info,id):
        entries = Entry.objects.get(pk=id)
        entries.delete()
        return(EntryDeleteMutation(entries=None))
        
class Mutation:
    create_entry = EntryCreateMutation.Field()
    update_entry = EntryUpdateMutation.Field()
    delete_entry = EntryDeleteMutation.Field()
    token_auth = relay_auth.ObtainJSONWebToken.Field()
    verify_token = relay_auth.VerifyToken.Field()