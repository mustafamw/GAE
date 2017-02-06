from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages
from egb.generic.product import ProductType
from egb.generic.product import ProductVariation
from egb.generic.pmi import WhoLevel, StatusType, CoverLevel, CoverWhere
from egb.user.user import UserModel
from egb.name_field.name_field import ManagerField, EmployeeField


class PmiTrs(messages.Message):
    premium_who = messages.EnumField(WhoLevel, 1, required=False)
    premium_cover_level = messages.EnumField(CoverLevel, 2, required=False)
    premium_core = messages.FloatField(3, required=True)

   
class PMI(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    provider_name = messages.StringField(2, required=False)
    product_type = messages.EnumField(ProductType, 3, required=False)
    product_variation = messages.EnumField(ProductVariation, 4, required=False)
    flexible = messages.BooleanField(5, required=False)
    who = messages.EnumField(WhoLevel, 6, required=True)
    premium_who = messages.EnumField(WhoLevel, 7, required=True)
    cover_level = messages.EnumField(CoverLevel, 8, required=True)
    premium_cover_level = messages.EnumField(CoverLevel, 9, required=True)
    where = messages.EnumField(CoverWhere, 10, required=True)
    excess = messages.FloatField(11, required=False)
    premium_core = messages.FloatField(12, required=False)
    gross_cost = messages.FloatField(13, required=False)
    pmi_key = messages.IntegerField(14, required=True)
    
    
class PMIList(messages.Message):
    pmi_list = messages.MessageField(PMI, 1, repeated=True)
                                     
                                     
class PMIModel(ndb.Model):
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    provider_name = ndb.StringProperty(required=True)
    product_type = msgprop.EnumProperty(ProductType, required=True, indexed=True)
    product_variation = msgprop.EnumProperty(ProductVariation, required=True, indexed=True)
    flexible = ndb.BooleanProperty(required=False) 
    who = msgprop.EnumProperty(WhoLevel, required=True, indexed=True)
    premium_who = msgprop.EnumProperty(WhoLevel, required=True, indexed=True)
    cover_level = msgprop.EnumProperty(CoverLevel, required=True, indexed=True)
    premium_cover_level = msgprop.EnumProperty(CoverLevel, required=True, indexed=True)  
    where = msgprop.EnumProperty(CoverWhere, required=True, indexed=True)        
    excess = ndb.FloatProperty(required=False)   
    premium_core = ndb.FloatProperty(required=False)
    gross_cost = ndb.FloatProperty(required=True)
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
        

class PMISignupResponse(messages.Message):
    message = messages.StringField(1)       
    
    
class PMISignup(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    pmi_signup_key = messages.IntegerField(2, required=True)
    who = messages.EnumField(WhoLevel, 3, required=True)
    excess = messages.FloatField(4, required=True)
    gross_cost = messages.FloatField(5, required=True)
    token = messages.StringField(6, required=True)
    status = messages.EnumField(StatusType, 7, required=True)
    submitted = messages.StringField(8, required=True)
    manager = messages.MessageField(ManagerField, 9)
    employee = messages.MessageField(EmployeeField, 10)
    
class PMISignupList(messages.Message):
    pmi_signup_list = messages.MessageField(PMISignup, 1, repeated=True)
    

class PMISignupModel(ndb.Model):
    pmi = ndb.KeyProperty(kind=PMIModel, required=True)
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    who = msgprop.EnumProperty(WhoLevel, required=True)
    excess = ndb.FloatProperty(required=True)
    gross_cost = ndb.FloatProperty(required=True)
    token = ndb.StringProperty(required=True) 
    status = msgprop.EnumProperty(StatusType, required=True)
    submitted = ndb.DateTimeProperty(auto_now_add=True)
    manager = ndb.KeyProperty(kind=UserModel, required=False) 
