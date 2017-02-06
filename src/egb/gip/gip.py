from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages
from egb.generic.product import ProductType
from egb.generic.product import ProductVariation
from egb.generic.gip import DeferredType, PaymentTermType
from egb.user.user import UserModel
from egb.generic.gip import StatusType 
from egb.name_field.name_field import ManagerField, EmployeeField
from egb.employee.employee import EmployeeModel


class GipTrs(messages.Message):
    premium_core = messages.FloatField(1, required=True)
   
class Gip(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    provider_name = messages.StringField(2, required=False)
    product_type = messages.EnumField(ProductType,3, required=False)
    product_variation = messages.EnumField(ProductVariation, 4, required=False)
    percentage = messages.FloatField(5, required=False)
    premium_percentage = messages.FloatField(6, required=False)
    deferred_period = messages.EnumField(DeferredType, 7, required=False)
    payment_term = messages.EnumField(PaymentTermType, 8, required=False)
    flexible = messages.BooleanField(9, required=False)
    free_cover_limit = messages.FloatField(10, required=False)
    payment_period = messages.FloatField(11, required=False)
    premium_core = messages.FloatField(12, required=False)
    gross_cost = messages.FloatField(13, required=False)
    window_salary = messages.FloatField(14, required=False)
    
class GipList(messages.Message):
    gip_list = messages.MessageField(Gip, 1, repeated=True)
                                     
    
class GipModel(ndb.Model):
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    provider_name = ndb.StringProperty(required=True)
    product_type = msgprop.EnumProperty(ProductType, required=True, indexed=True)
    product_variation = msgprop.EnumProperty(ProductVariation, required=True, indexed=True)
    percentage = ndb.FloatProperty(required=False)
    premium_percentage = ndb.FloatProperty(required=False)     
    deferred_period = msgprop.EnumProperty(DeferredType, required=True, indexed=True)
    payment_term = msgprop.EnumProperty(PaymentTermType, required=True, indexed=True)
    flexible = ndb.BooleanProperty(required=False)
    free_cover_limit = ndb.FloatProperty(required=False)
    payment_period = ndb.FloatProperty(required=False)
    premium_core = ndb.FloatProperty(required=False)
    gross_cost = ndb.FloatProperty(required=True)
    window_salary = ndb.FloatProperty(required=True)
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
        

class GipSignupModel(ndb.Model):
    gip = ndb.KeyProperty(kind=GipModel, required=True)
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    window_salary = ndb.ComputedProperty(lambda self: EmployeeModel.get_employee_salary(self.user, self.user_id))
    percentage = ndb.FloatProperty(required=True)
    deferred_period = msgprop.EnumProperty(DeferredType, required=False) 
    payment_term = msgprop.EnumProperty(PaymentTermType, required=True) 
    gross_cost = ndb.FloatProperty(required=True)
    status = msgprop.EnumProperty(StatusType, required=True)
    token = ndb.StringProperty(required=True)
    manager = ndb.KeyProperty(kind=UserModel)
    submitted = ndb.DateTimeProperty(auto_now_add=True)
    

class GipSignup(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    gip_signup_key = messages.IntegerField(2, required=True)
    window_salary = messages.FloatField(3, required=True)
    percentage = messages.FloatField(4, required=True)
    deferred_period = messages.EnumField(DeferredType, 5, required=False)
    payment_term = messages.EnumField(PaymentTermType, 6, required=True)
    gross_cost = messages.FloatField(7, required=True)
    status = messages.EnumField(StatusType, 8, required=True)
    submitted = messages.StringField(9, required=True)
    token = messages.StringField(10, required=True)
    manager = messages.MessageField(ManagerField, 11)
    employee = messages.MessageField(EmployeeField, 12)
    

class GipSignupList(messages.Message):
    gip_signup_list = messages.MessageField(GipSignup, 1, repeated=True)
    
    
class GipSignupResponse(messages.Message):
    message = messages.StringField(1, required=False)

