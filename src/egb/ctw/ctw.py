from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages
from egb.generic.product import ProductType
from egb.generic.product import ProductVariation
from egb.generic.ctw import StatusType
from egb.user.user import UserModel
from egb.name_field.name_field import ManagerField, EmployeeField


class CtwSignupResponse(messages.Message):   
    message = messages.StringField(1, required=True)
    
    
class Ctw(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    provider_name = messages.StringField(2, required=False)
    product_type = messages.EnumField(ProductType, 3, required=False)
    product_variation = messages.EnumField(ProductVariation, 4, required=False)
    gross_cost = messages.FloatField(5, required=False)
    status = messages.EnumField(StatusType, 6, required=False)
    submitted = messages.StringField(7, required=True)
    
class CtwList(messages.Message):
    ctw_list = messages.MessageField(Ctw, 1, repeated=True)
    

class CtwSignup(messages.Message):
    ctw_signup_key = messages.IntegerField(1, required=True)
    user_id = messages.IntegerField(2, required=True)
    provider_name = messages.StringField(3, required=False)
    product_type = messages.EnumField(ProductType, 4, required=False)
    product_variation = messages.EnumField(ProductVariation, 5, required=False)
    gross_cost = messages.FloatField(6, required=False)
    status = messages.EnumField(StatusType, 7, required=False)
    submitted = messages.StringField(8, required=True)
    employee = messages.MessageField(EmployeeField, 9)
    manager = messages.MessageField(ManagerField, 10)
    token = messages.StringField(11, required=True)
    
class CtwSignupList(messages.Message):
    ctw_signup_list = messages.MessageField(CtwSignup, 1, repeated=True)
                                     
                                     
class CtwModel(ndb.Model):
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    provider_name = ndb.StringProperty(required=True)
    product_type = msgprop.EnumProperty(ProductType, required=True, indexed=True)
    product_variation = msgprop.EnumProperty(ProductVariation, required=True, indexed=True)
    gross_cost = ndb.FloatProperty(required=True)
    status = msgprop.EnumProperty(StatusType, required=True, indexed=True)
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


class CtwSignupModel(ndb.Model):
    ctw =  ndb.KeyProperty(kind=CtwModel)
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    provider_name = ndb.StringProperty(required=True)
    product_type = msgprop.EnumProperty(ProductType, required=True, indexed=True)
    product_variation = msgprop.EnumProperty(ProductVariation, required=True, indexed=True)
    gross_cost = ndb.FloatProperty(required=True)
    status = msgprop.EnumProperty(StatusType, required=True, indexed=True)
    token = ndb.StringProperty(required=True)
    submitted = ndb.DateTimeProperty(auto_now_add=True) 
    manager = ndb.KeyProperty(kind=UserModel, required=False) 


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
    