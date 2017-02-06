from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages
from egb.generic.product import ProductType
from egb.generic.product import ProductVariation
    
class Provider(messages.Message):
    provider_name = messages.StringField(1, required=True)
    product_type = messages.EnumField(ProductType, 2, required=True)
    product_variation = messages.EnumField(ProductVariation, 3, required=True)
    web_link = messages.StringField(4, required=True)
    icon_link = messages.StringField(5, required=True)
    bumf = messages.StringField(6, required=True)

class ProviderList(messages.Message):
    provider_list = messages.MessageField(Provider, 1, repeated=True) 
    
class ProviderModel(ndb.Model):
    provider_name = ndb.StringProperty(required=True)
    product_type = msgprop.EnumProperty(ProductType, required=True, indexed=True)
    product_variation = msgprop.EnumProperty(ProductVariation, required=True, indexed=True)
    web_link = ndb.StringProperty(required=True)
    icon_link = ndb.StringProperty(required=True)
    bumf = ndb.StringProperty(required=True)
    submitted = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_count(cls):
        return cls.query().count()
    
    @classmethod
    def get_submitted(cls):
        dateSubmitted = cls.query().order(-cls.submitted).get();
        if dateSubmitted:
            return dateSubmitted.submitted
        else:
            return False 
    
    
    