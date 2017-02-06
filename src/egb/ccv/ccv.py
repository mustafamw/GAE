from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages
from egb.generic.product import ProductType
from egb.generic.product import ProductVariation
from egb.name_field.name_field import ManagerField, EmployeeField
from egb.generic.ccv import StatusType

from egb.user.user import UserModel

   
class Ccv(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    provider_name = messages.StringField(2, required=False)
    product_type = messages.EnumField(ProductType, 3, required=False)
    product_variation = messages.EnumField(ProductVariation, 4, required=False)
    contribution = messages.FloatField(5, required=False)
    protected_rights = messages.BooleanField(6, required=False)
    
class CcvList(messages.Message):
    ccv_list = messages.MessageField(Ccv, 1, repeated=True)
                                                                      
class CcvModel(ndb.Model):
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    provider_name = ndb.StringProperty(required=True)
    product_type = msgprop.EnumProperty(ProductType, required=True, indexed=True)
    product_variation = msgprop.EnumProperty(ProductVariation, required=True, indexed=True)
    contribution = ndb.FloatProperty(required=True)
    protected_rights = ndb.BooleanProperty(required=False) 
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
        
class CcvSignupResponse(messages.Message):
    message = messages.StringField(1, required=True)
    

class CcvSignup(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    ccv_signup_key = messages.IntegerField(2, required=True)
    contribution = messages.FloatField(3, required=True)
    comment = messages.StringField(4, required=False)
    token = messages.StringField(5, required=True)
    status = messages.EnumField(StatusType, 6, required=True)
    submitted = messages.StringField(7, required=True)
    employee = messages.MessageField(EmployeeField, 8)
    manager = messages.MessageField(ManagerField, 9)
    
class CcvSignupList(messages.Message):
    ccv_signup_list = messages.MessageField(CcvSignup, 1, repeated=True)

class CcvSignupModel(ndb.Model):
    ccv = ndb.KeyProperty(kind=CcvModel, required=True)
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    contribution = ndb.FloatProperty(required=True)
    comment = ndb.TextProperty(required=False)
    status = ndb.msgprop.EnumProperty(StatusType, required=True)
    token = ndb.StringProperty(required=True)
    submitted = ndb.DateTimeProperty(auto_now_add=True)
    manager = ndb.KeyProperty(kind=UserModel, required=False, indexed=False)
