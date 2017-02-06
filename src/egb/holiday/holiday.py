from google.appengine.ext import ndb
from google.appengine.ext.ndb import msgprop
from protorpc import messages
from egb.user.user import UserModel
from egb.generic.holiday import HolidayHalfDay
from egb.generic.holiday import Status
from egb.generic.holiday import Allowance
from egb.name_field.name_field import ManagerField
from egb.name_field.name_field import EmployeeField
   
class Holiday(messages.Message):
    holiday_key = messages.IntegerField(1, required=True)
    user_id = messages.IntegerField(2, required=True)
    team = messages.StringField(3, required=True)
    days_off = messages.StringField(4, repeated=True)    
    allowance = messages.FloatField(5, required=False)
    allowance_type = messages.EnumField(Allowance, 6, required=False)
    year = messages.IntegerField(7, required=True)
    employee = messages.MessageField(EmployeeField, 8, required=False)
    
class HolidayDetailList(messages.Message):
    holiday_detail_list = messages.MessageField(Holiday, 1, repeated=True)
    

class HolidayDetailResponse(messages.Message):
    message = messages.StringField(1, required=True);
    

class HolidayBook(messages.Message):
    holiday_book_key = messages.IntegerField(1, required=False);
    user_id = messages.IntegerField(2, required=False);
    start_date = messages.StringField(3, required=False);
    end_date = messages.StringField(4, required=False);
    start_halfday = messages.EnumField(HolidayHalfDay, 5, required=True)
    end_halfday = messages.EnumField(HolidayHalfDay, 6, required=True)
    taken = messages.FloatField(7, required=False);
    status = messages.EnumField(Status, 8, required=False);
    submitted = messages.StringField(9, required=False);
    token = messages.StringField(10, required=False);
    manager = messages.MessageField(ManagerField, 11)
    employee = messages.MessageField(EmployeeField, 12)
    allowance_type = messages.EnumField(Allowance, 13, required=False)
    

class HolidayBookList(messages.Message):
    holiday_book_list = messages.MessageField(HolidayBook, 1, repeated=True);
    

class HolidayBookResponse(messages.Message):
    message = messages.StringField(1, required=False);
    
    
    
class HolidayModel(ndb.Model):
    user = ndb.KeyProperty(kind=UserModel)
    user_id = ndb.IntegerProperty(required=True) 
    team = ndb.StringProperty(required=True)
    days_off = ndb.StringProperty(repeated=True, indexed=False) 
    allowance = ndb.FloatProperty(required=False, default=0.0, indexed=False) 
    allowance_type = msgprop.EnumProperty(Allowance, required=True, indexed=False)
    year = ndb.IntegerProperty(required=False)
    submitted = ndb.DateTimeProperty(auto_now_add=True)
    
    @classmethod
    def get_count(cls):
        return cls.query().count()
    
    @classmethod
    def get_submitted(cls):
        dateSubmitted = cls.query().order(-cls.submitted).get()
        if dateSubmitted:
            return dateSubmitted.submitted
        else:
            return False 
    

class HolidayBookModel(ndb.Model):
    holiday = ndb.KeyProperty(kind=HolidayModel)
    user = ndb.KeyProperty(kind=UserModel)
    user_id = ndb.IntegerProperty();
    start_date = ndb.DateProperty();
    end_date = ndb.DateProperty();
    start_halfday = msgprop.EnumProperty(HolidayHalfDay)
    end_halfday = msgprop.EnumProperty(HolidayHalfDay)
    taken = ndb.FloatProperty();
    status = msgprop.EnumProperty(Status)
    token = ndb.StringProperty();
    allowance_type = msgprop.EnumProperty(Allowance, required=True, indexed=False)
    submitted = ndb.DateTimeProperty(auto_now_add=True)
    manager = ndb.KeyProperty(kind=UserModel)
    
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
    
    
    

    
    

    
    