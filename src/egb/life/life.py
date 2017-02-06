from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages
from egb.generic.product import ProductType
from egb.generic.product import ProductVariation
from egb.generic.life import StatusType 
from egb.user.user import UserModel
from egb.name_field.name_field import ManagerField, EmployeeField
from egb.employee.employee import EmployeeModel

class LifeTrs(messages.Message):
    premium_core = messages.FloatField(1, required=False)
    core_multiple = messages.FloatField(2, required=False)

   
class Life(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    provider_name = messages.StringField(2, required=False)
    product_type = messages.EnumField(ProductType, 3, required=False)
    product_variation = messages.EnumField(ProductVariation, 4, required=False)
    calculate = messages.BooleanField(5, required=False)
    sum_assured = messages.FloatField(6, required=False)
    core_multiple = messages.FloatField(7, required=False)
    flexible = messages.BooleanField(8, required=False)
    flex_multiple = messages.FloatField(9, required=False)
    flex_max_multiple = messages.FloatField(10, required=False)
    free_cover_limit = messages.FloatField(11, required=False)
    cap = messages.FloatField(12, required=False)
    premium_core = messages.FloatField(13, required=False)
    premium_flex = messages.FloatField(14, required=False)
    gross_cost = messages.FloatField(15, required=False)
    wish_expression_link = messages.StringField(16, required=False)
    life_key = messages.IntegerField(17, required=True)
    window_salary = messages.FloatField(18, required=False)
    
class LifeList(messages.Message):
    life_list = messages.MessageField(Life, 1, repeated=True)
                                     
    
class LifeModel(ndb.Model):
    user = ndb.KeyProperty(kind=UserModel, required=True)
    user_id = ndb.IntegerProperty(required=True)
    provider_name = ndb.StringProperty(required=True)
    product_type = msgprop.EnumProperty(ProductType, required=True, indexed=True)
    product_variation = msgprop.EnumProperty(ProductVariation, required=True, indexed=True)
    calculate = ndb.BooleanProperty(required=False)    
    sum_assured = ndb.FloatProperty(required=False)
    core_multiple = ndb.FloatProperty(required=True)
    window_salary = ndb.FloatProperty(required=True)
    flexible = ndb.BooleanProperty(required=False) 
    flex_multiple = ndb.FloatProperty(required=False)
    flex_max_multiple = ndb.FloatProperty(required=False)
    free_cover_limit = ndb.FloatProperty(required=False)
    cap = ndb.FloatProperty(required=False)
    premium_core = ndb.FloatProperty(required=False)
    gross_cost = ndb.FloatProperty(required=True)
    wish_expression_link = ndb.StringProperty(required=True)
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
        

class LifeSignup(messages.Message):
    user_id = messages.IntegerField(1, required=True)
    life_signup_key = messages.IntegerField(2, required=True)
    window_salary = messages.FloatField(3, required=True)
    multiple = messages.FloatField(4, required=True)
    gross_cost = messages.FloatField(5, required=True)
    status = messages.EnumField(StatusType, 6, required=True)
    submitted = messages.StringField(7, required=True)
    token = messages.StringField(8, required=True)
    manager = messages.MessageField(ManagerField, 9)
    employee = messages.MessageField(EmployeeField, 10)
        
class LifeSignupList(messages.Message):
    life_signup_list = messages.MessageField(LifeSignup, 1, repeated=True)

class LifeSignupModel(ndb.Model):
    life = ndb.KeyProperty(kind=LifeModel)
    user = ndb.KeyProperty(kind=UserModel)
    user_id = ndb.IntegerProperty(required=True)
    window_salary = ndb.ComputedProperty(lambda self: EmployeeModel.get_employee_salary(self.user, self.user_id))
    multiple = ndb.FloatProperty(required=True, indexed=False)
    gross_cost = ndb.FloatProperty(required=True, indexed=False)
    status = msgprop.EnumProperty(StatusType, required=True, indexed=True)
    submitted = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    token = ndb.StringProperty(required=True, indexed=True)
    manager = ndb.KeyProperty(kind=UserModel, required=False, indexed=False)
    
    

class LifeSignupResponse(messages.Message):
    message = messages.StringField(1, required=False)
    
