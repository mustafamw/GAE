from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop

from protorpc import messages

from egb.generic.product import ProductType
from egb.generic.product import ProductVariation
from egb.generic.health_assessment import WhoLevel, CoverLevel

from egb.user.user import UserModel
   
class HealthAssessment(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    provider_name = messages.StringField(2, required=False)
    product_type = messages.EnumField(ProductType, 3, required=False)
    product_variation = messages.EnumField(ProductVariation, 4, required=False)
    flexible = messages.BooleanField(5, required=False)
    who = messages.EnumField(WhoLevel, 6, required=True)
    cover_level = messages.EnumField(CoverLevel, 7, required=True)
    premium_core = messages.FloatField(8, required=False)
    premium_flex = messages.FloatField(9, required=False)
    gross_cost = messages.FloatField(10, required=False)
    net = messages.FloatField(11, required=False)
    
class HealthAssessmentList(messages.Message):
    health_assessment_list = messages.MessageField(HealthAssessment, 1, repeated=True)
                                     
class HealthAssessmentModel(ndb.Model):
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    provider_name = ndb.StringProperty(required=True)
    product_type = msgprop.EnumProperty(ProductType, required=True, indexed=True)
    product_variation = msgprop.EnumProperty(ProductVariation, required=True, indexed=True)
    flexible = ndb.BooleanProperty(required=False) 
    who = msgprop.EnumProperty(WhoLevel, required=True, indexed=True)
    cover_level = msgprop.EnumProperty(CoverLevel, required=True, indexed=True)
    premium_core = ndb.FloatProperty(required=False)
    premium_flex = ndb.FloatProperty(required=False)
    gross_cost = ndb.FloatProperty(required=True)
    net = ndb.FloatProperty(required=True)
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
