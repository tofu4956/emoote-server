from datetime import date

from django.contrib.auth import login
import graphene
from graphene import relay
from graphene.types import field
from graphql_auth import relay as relay_auth
from .models import Entry
from graphene_django.types import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphene_django.filter import DjangoFilterConnectionField

class EntryType(DjangoObjectType):
    class Meta:
        model = Entry
        field = ("id", "uid", "createdtime", "entry")
        
class EntryNode(DjangoObjectType):
    class Meta:
        model = Entry
        filter_fields = ['id','uid', 'createdtime', 'entry']
        interfaces = (relay.Node, )

class Query(graphene.ObjectType):
    all_Entry = DjangoFilterConnectionField(EntryNode)
    entry = relay.Node.Field(EntryNode)
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
        uid = graphene.ID()
        createdtime = graphene.Date(required=True)
        entry = graphene.String(required=True)
    entry = graphene.Field(EntryType)
    def mutate(self,info,uid,createdtime,entry):
        entry = Entry.objects.create(uid=uid,createdtime=createdtime,entry=entry)
        return EntryCreateMutation(entry=entry)
    
class EntryUpdateMutation(graphene.Mutation):
    class Arguments:
        uid = graphene.ID(required=True)
        createdtime = graphene.Date(required=True)
        entry = graphene.String()
    entry = graphene.Field(EntryType)
    def mutate(self,info,uid,createdtime,entry):
        entries = Entry.objects.get(pk=uid)
        entries.save()
        return EntryUpdateMutation(entries=entries)

class EntryDeleteMutation(graphene.Mutation):
    class Arguments:
        uid = graphene.ID()
    entry = graphene.Field(EntryType)
    def mutate(self,info,uid):
        entries = Entry.objects.get(pk=uid)
        entries.delete()
        return(EntryDeleteMutation(entries=None))
        
class Mutation:
    create_entry = EntryCreateMutation.Field()
    update_entry = EntryUpdateMutation.Field()
    delete_entry = EntryDeleteMutation.Field()
    token_auth = relay_auth.ObtainJSONWebToken.Field()
    verify_token = relay_auth.VerifyToken.Field()