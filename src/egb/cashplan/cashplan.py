from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages
from egb.generic.product import ProductType
from egb.generic.product import ProductVariation
from egb.generic.cashplan import WhoLevel, StatusType, CoverLevel
from egb.name_field.name_field import ManagerField, EmployeeField
from egb.user.user import UserModel

class CashplanTrs(messages.Message):
    premium_who = messages.EnumField(WhoLevel, 1, required=False)
    premium_cover_level = messages.EnumField(CoverLevel, 2, required=False)
    premium_core = messages.FloatField(3, required=True)

class Cashplan(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    provider_name = messages.StringField(2, required=False)
    product_type = messages.EnumField(ProductType, 3, required=False)
    product_variation = messages.EnumField(ProductVariation, 4, required=False)
    who = messages.EnumField(WhoLevel, 5, required=True)
    premium_who = messages.EnumField(WhoLevel, 6, required=True)
    cover_level = messages.EnumField(CoverLevel, 7, required=True)
    premium_cover_level = messages.EnumField(CoverLevel, 8, required=True)
    premium_core = messages.FloatField(9, required=False)
    gross_cost = messages.FloatField(10, required=False)
    cashplan_key = messages.IntegerField(11, required=True)

class CashplanList(messages.Message):
    cashplan_list = messages.MessageField(Cashplan, 1, repeated=True)
                                     
                                                            
class CashplanModel(ndb.Model):
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    provider_name = ndb.StringProperty(required=True)
    product_type = msgprop.EnumProperty(ProductType, required=True, indexed=True)
    product_variation = msgprop.EnumProperty(ProductVariation, required=True, indexed=True)
    who = msgprop.EnumProperty(WhoLevel, required=True, indexed=True)
    premium_who = msgprop.EnumProperty(WhoLevel, required=True, indexed=True)
    cover_level = msgprop.EnumProperty(CoverLevel, required=True, indexed=True)
    premium_cover_level = msgprop.EnumProperty(CoverLevel, required=True, indexed=True)           
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


class CashplanSignupResponse(messages.Message):
    message = messages.StringField(1)       
    
    
class CashplanSignup(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    cashplan_signup_key = messages.IntegerField(2, required=True)
    who = messages.EnumField(WhoLevel, 3, required=True)
    cover_level = messages.EnumField(CoverLevel, 4, required=True)
    gross_cost = messages.FloatField(5, required=True)
    token = messages.StringField(6, required=True)
    status = messages.EnumField(StatusType, 7, required=True)
    submitted = messages.StringField(8, required=True)
    employee = messages.MessageField(EmployeeField, 9)
    manager = messages.MessageField(ManagerField, 10)
    
class CashplanSignupList(messages.Message):
    cashplan_signup_list = messages.MessageField(CashplanSignup, 1, repeated=True)
    

class CashplanSignupModel(ndb.Model):
    cashplan = ndb.KeyProperty(kind=CashplanModel, required=True)
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    who = msgprop.EnumProperty(WhoLevel, required=True)
    cover_level = msgprop.EnumProperty(CoverLevel, required=True)
    gross_cost = ndb.FloatProperty(required=True)
    token = ndb.StringProperty(required=True) 
    status = msgprop.EnumProperty(StatusType, required=True)
    submitted = ndb.DateTimeProperty(auto_now_add=True)
    manager = ndb.KeyProperty(kind=UserModel, required=False) 
        
